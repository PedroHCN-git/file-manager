from pydantic import BaseModel, Field
from typing import Optional

class DocumentModel(BaseModel):

    doc_id: int
    doc_name: str
    doc_path: Optional[str] = Field(default=None)