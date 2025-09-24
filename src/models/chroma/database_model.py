import os
from typing import Optional
import chromadb
from chromadb.config import Settings
from ...utils.logger import setup_logger


class DatabaseModel:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.client: Optional[chromadb.Client] = None
        self.collection_name = "knowledge_base"
        self._initialize_client()

    def _initialize_client(self):
        try:
            persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            self.logger.info(f"ChromaDB client initialized with persist directory: {persist_directory}")

        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB client: {e}")
            self.client = None

    def get_or_create_collection(self, collection_name: Optional[str] = None):
        if not self.client:
            raise Exception("ChromaDB client not initialized")

        name = collection_name or self.collection_name

        try:
            collection = self.client.get_or_create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
            self.logger.debug(f"Retrieved/created collection: {name}")
            return collection

        except Exception as e:
            self.logger.error(f"Failed to get/create collection {name}: {e}")
            raise

    def reset_database(self) -> bool:
        try:
            if self.client:
                self.client.reset()
                self.logger.info("ChromaDB database reset successfully")
                return True
            return False

        except Exception as e:
            self.logger.error(f"Failed to reset database: {e}")
            return False