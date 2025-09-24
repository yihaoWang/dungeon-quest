from pydantic import BaseModel
from typing import Dict, Optional, Any
from datetime import datetime
import json


class KnowledgeBase(BaseModel):
    id: Optional[str] = None
    content_type: str
    content_id: str
    title: str
    content: str
    metadata: Dict[str, Any] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        extra = "allow"

    def to_chroma_document(self):
        flat_metadata = {
            "content_type": self.content_type,
            "content_id": self.content_id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            **{
                key: value if isinstance(value, (str, int, float, bool)) or value is None
                else json.dumps(value, ensure_ascii=False)
                for key, value in self.metadata.items()
            }
        }

        return {
            "id": f"{self.content_type}_{self.content_id}",
            "document": self.content,
            "metadata": flat_metadata
        }

    @classmethod
    def from_chroma_result(cls, doc_id: str, document: str, metadata: Dict):
        return cls(
            id=doc_id,
            content_type=metadata.get("content_type", "unknown"),
            content_id=metadata.get("content_id", doc_id),
            title=metadata.get("title", "Unknown"),
            content=document,
            metadata={
                k: v for k, v in metadata.items()
                if k not in ["content_type", "content_id", "title", "created_at", "updated_at"]
            },
            created_at=datetime.fromisoformat(metadata["created_at"]) if metadata.get("created_at") else None,
            updated_at=datetime.fromisoformat(metadata["updated_at"]) if metadata.get("updated_at") else None,
        )