import os
from typing import List, Optional
from openai import AsyncOpenAI
from ...utils.logger import setup_logger


class EmbeddingModel:

    def __init__(self):
        self.logger = setup_logger(__name__)
        self.client: Optional[AsyncOpenAI] = None
        self._initialize_client()

    def _initialize_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.client = AsyncOpenAI(api_key=api_key)
                self.logger.info("OpenAI client initialized for embeddings")
            except Exception as e:
                self.logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            self.logger.warning("No OpenAI API key found - embeddings unavailable")

    async def get_embedding(self, text: str) -> Optional[List[float]]:
        if not self.client:
            return None

        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text.replace("\n", " ")
            )
            embedding = response.data[0].embedding
            self.logger.debug(f"Generated embedding for text: {text[:100]}...")
            return embedding

        except Exception as e:
            self.logger.error(f"Failed to generate embedding: {e}")
            return None
