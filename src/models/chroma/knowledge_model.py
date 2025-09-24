"""
KnowledgeModel for managing knowledge entries in ChromaDB
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from .database_model import DatabaseModel
from .embedding_model import EmbeddingModel
from .knowledge_base import KnowledgeBase
from ...utils.logger import setup_logger


class KnowledgeModel:

    def __init__(self, database_model: DatabaseModel, embedding_model: EmbeddingModel):
        self.logger = setup_logger(__name__)
        self.db = database_model
        self.embedding_model = embedding_model

    async def store_knowledge(self, content_type: str, content_id: str,
                            title: str, content: str, metadata: Dict = None) -> bool:
        try:
            # Create knowledge base entry
            knowledge = KnowledgeBase(
                content_type=content_type,
                content_id=content_id,
                title=title,
                content=content,
                metadata=metadata or {},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            # Get embedding
            embedding = await self.embedding_model.get_embedding(content)

            # Get collection
            collection = self.db.get_or_create_collection()

            # Convert to ChromaDB format
            doc_data = knowledge.to_chroma_document()

            # Store in ChromaDB
            collection.add(
                ids=[doc_data["id"]],
                documents=[doc_data["document"]],
                metadatas=[doc_data["metadata"]],
                embeddings=[embedding] if embedding else None
            )

            self.logger.debug(f"Stored knowledge: {content_type}/{content_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store knowledge {content_type}/{content_id}: {e}")
            return False

    async def ingest_game_data(self, monsters_data: Dict, items_data: Dict) -> bool:
        try:
            success_count = 0
            total_count = 0

            # Ingest monsters
            for monster_id, monster_data in monsters_data.items():
                total_count += 1
                content = f"Name: {monster_data.get('name', monster_id)}\n"
                content += f"Description: {monster_data.get('description', 'No description available.')}\n"

                if 'stats' in monster_data:
                    stats = monster_data['stats']
                    content += f"HP: {stats.get('hp', 'Unknown')}, "
                    content += f"Attack: {stats.get('attack', 'Unknown')}, "
                    content += f"Defense: {stats.get('defense', 'Unknown')}\n"

                if 'abilities' in monster_data:
                    content += f"Abilities: {', '.join(monster_data['abilities'])}\n"

                success = await self.store_knowledge(
                    content_type="monster",
                    content_id=monster_id,
                    title=monster_data.get('name', monster_id),
                    content=content,
                    metadata=monster_data
                )

                if success:
                    success_count += 1

            # Ingest items
            for item_id, item_data in items_data.items():
                total_count += 1
                content = f"Name: {item_data.get('name', item_id)}\n"
                content += f"Description: {item_data.get('description', 'No description available.')}\n"
                content += f"Type: {item_data.get('type', 'Unknown')}\n"

                if 'effects' in item_data:
                    content += f"Effects: {item_data['effects']}\n"

                if 'value' in item_data:
                    content += f"Value: {item_data['value']}\n"

                success = await self.store_knowledge(
                    content_type="item",
                    content_id=item_id,
                    title=item_data.get('name', item_id),
                    content=content,
                    metadata=item_data
                )

                if success:
                    success_count += 1

            self.logger.info(f"Ingested {success_count}/{total_count} knowledge entries")
            return success_count == total_count

        except Exception as e:
            self.logger.error(f"Failed to ingest game data: {e}")
            return False

    def get_all_knowledge(self, content_type: Optional[str] = None) -> List[KnowledgeBase]:
        try:
            collection = self.db.get_or_create_collection()

            where_clause = {"content_type": content_type} if content_type else None

            results = collection.get(
                where=where_clause,
                include=["documents", "metadatas"]
            )

            knowledge_list = []
            if results['ids']:
                for i, doc_id in enumerate(results['ids']):
                    knowledge = KnowledgeBase.from_chroma_result(
                        doc_id=doc_id,
                        document=results['documents'][i],
                        metadata=results['metadatas'][i]
                    )
                    knowledge_list.append(knowledge)

            return knowledge_list

        except Exception as e:
            self.logger.error(f"Failed to get all knowledge: {e}")
            return []

    def clear_knowledge(self, content_type: Optional[str] = None) -> int:
        try:
            collection = self.db.get_or_create_collection()

            if content_type:
                # Get IDs to delete
                results = collection.get(
                    where={"content_type": content_type},
                    include=[]
                )
                if results['ids']:
                    collection.delete(ids=results['ids'])
                    count = len(results['ids'])
                else:
                    count = 0
            else:
                # Clear all
                count = collection.count()
                collection.delete()

            self.logger.info(f"Cleared {count} knowledge entries")
            return count

        except Exception as e:
            self.logger.error(f"Failed to clear knowledge: {e}")
            return 0