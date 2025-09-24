import os
from typing import List, Dict, Any, Optional
from ..utils.logger import setup_logger
from ..models.chroma import (
    DatabaseModel,
    EmbeddingModel,
    SearchModel,
    KnowledgeModel
)


class VectorService:

    def __init__(self):
        self.logger = setup_logger(__name__)

        self.database_model = DatabaseModel()
        self.embedding_model = EmbeddingModel()
        self.search_model = SearchModel(self.database_model, self.embedding_model)
        self.knowledge_model = KnowledgeModel(self.database_model, self.embedding_model)


    async def get_embedding(self, text: str) -> Optional[List[float]]:
        return await self.embedding_model.get_embedding(text)

    async def store_knowledge(self, content_type: str, content_id: str,
                            title: str, content: str, metadata: Dict = None) -> bool:
        return await self.knowledge_model.store_knowledge(
            content_type=content_type,
            content_id=content_id,
            title=title,
            content=content,
            metadata=metadata
        )

    async def semantic_search(self, query: str, content_type: Optional[str] = None,
                            limit: int = 5, similarity_threshold: float = 0.7,
                            game_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return await self.search_model.semantic_search(
            query=query,
            content_type=content_type,
            limit=limit,
            similarity_threshold=similarity_threshold,
            game_id=game_id
        )

    async def ingest_game_data(self, monsters_data: Dict, items_data: Dict) -> bool:
        return await self.knowledge_model.ingest_game_data(monsters_data, items_data)


    def get_knowledge_count(self, content_type: Optional[str] = None) -> int:
        return self.search_model.get_knowledge_count(content_type)

    async def close(self):
        self.logger.info("Vector service cleanup completed")




