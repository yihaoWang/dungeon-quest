import os
from openai import AsyncOpenAI
from ..utils.logger import setup_logger


class LLMService:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = AsyncOpenAI(api_key=api_key)
            self.logger.info("LLM service initialized with OpenAI client")
        else:
            self.client = AsyncOpenAI(api_key="dummy")
            self.logger.warning("No OpenAI API key found - using dummy client")

    def is_available(self) -> bool:
        return True

    def get_client(self) -> AsyncOpenAI:
        return self.client