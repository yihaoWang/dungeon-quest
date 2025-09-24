from typing import List, Dict, Any, Optional
from .database_model import DatabaseModel
from .embedding_model import EmbeddingModel
from ...utils.logger import setup_logger


class SearchModel:

    def __init__(self, database_model: DatabaseModel, embedding_model: EmbeddingModel):
        self.logger = setup_logger(__name__)
        self.db = database_model
        self.embedding_model = embedding_model

    async def semantic_search(self, query: str, content_type: Optional[str] = None,
                            limit: int = 5, similarity_threshold: float = 0.7,
                            game_id: Optional[str] = None) -> List[Dict[str, Any]]:
        try:
            query_embedding = await self.embedding_model.get_embedding(query)
            if not query_embedding:
                self.logger.error("Failed to get query embedding")
                return []

            collection = self.db.get_or_create_collection()

            # Prepare where clause for filtering
            where_clause = None
            if content_type and game_id:
                where_clause = {
                    "$and": [
                        {"content_type": {"$eq": content_type}},
                        {"game_id": {"$eq": game_id}}
                    ]
                }
            elif content_type:
                where_clause = {"content_type": {"$eq": content_type}}
            elif game_id:
                where_clause = {"game_id": {"$eq": game_id}}

            # Perform vector search
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause
            )

            # Convert results to standard format
            search_results = []
            if results['ids'] and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    distance = results['distances'][0][i] if results['distances'] else 0
                    similarity = 1 - distance  # Convert distance to similarity

                    if similarity >= similarity_threshold:
                        result = {
                            "id": doc_id,
                            "content": results['documents'][0][i],
                            "metadata": results['metadatas'][0][i],
                            "similarity": similarity,
                            "content_type": results['metadatas'][0][i].get("content_type"),
                            "title": results['metadatas'][0][i].get("title"),
                        }
                        search_results.append(result)

            self.logger.debug(f"Semantic search returned {len(search_results)} results for query: {query}")
            return search_results

        except Exception as e:
            self.logger.error(f"Semantic search failed: {e}")
            return []

    def get_knowledge_count(self, content_type: Optional[str] = None) -> int:
        try:
            collection = self.db.get_or_create_collection()

            if content_type:
                # Count with filter
                results = collection.get(
                    where={"content_type": content_type},
                    include=[]  # Don't include documents/metadata, just count
                )
                return len(results['ids']) if results['ids'] else 0
            else:
                # Count all
                return collection.count()

        except Exception as e:
            self.logger.error(f"Failed to get knowledge count: {e}")
            return 0