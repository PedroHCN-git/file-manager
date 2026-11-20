from backend.documents.document_model import DocumentSqlModel

from pydantic import BaseModel, model_validator
from typing import Optional

class DocumentIn(BaseModel):

    doc_id: None = None
    doc_name: str
    doc_path: str

class DocumentUpdate(BaseModel):

    doc_id: int
    doc_name: Optional[str]
    doc_path: Optional[str]

    @model_validator(mode="after")
    def check_blank_values(self):

        if not any([
            self.doc_id,
            self.doc_name,
            self.doc_path
        ]):
            raise ValueError("Pelo menos um campo deve ser preenchido")

        return self

class DocumentOut(BaseModel):

    doc_id: int
    doc_name: str

class DocumentFilter(BaseModel):

    doc_id: Optional[int]
    doc_name: Optional[str]

    @model_validator(mode="after")
    def check_blank_values(self):
    
        if not any([
            self.doc_id,
            self.doc_name,
        ]):
            raise ValueError("Pelo menos um campo deve ser preenchido")

        return self

class DocumentMapper():

    def map_in(
        self,
        document: DocumentUpdate | DocumentIn,
        owner_user_id: int,
    ) -> DocumentSqlModel:
        return DocumentSqlModel(
            doc_id=document.doc_id,
            doc_name=document.doc_name,
            doc_path=document.doc_path,
            owner_user_id=owner_user_id,
        )

    def map_out(self, document: DocumentSqlModel):

        return DocumentOut(
            doc_id=document.doc_id,
            doc_name=document.doc_name
        )