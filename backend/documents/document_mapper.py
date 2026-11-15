from backend.documents.document_model import DocumentInfoSqlModel
from shared import Orientation, OrderBy

from pydantic import BaseModel, model_validator, Field
from typing import Optional

class DocumentInfo(BaseModel):

    doc_name: str
    doc_path: str
    doc_description: str
    doc_id: Optional[int] = Field(default=None)

class DocumentInfoUpdate(BaseModel):

    doc_id: int
    doc_name: Optional[str] = Field(default=None)
    doc_path: Optional[str] = Field(default=None)
    doc_description: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def check_blank_values(self):

        if not any([
            self.doc_name,
            self.doc_path
        ]):
            raise ValueError("Pelo menos um campo deve ser preenchido")

        return self

class DocumentInfoOut(BaseModel):

    doc_id: int
    doc_name: str
    doc_path: str
    doc_description: str

class DocumentInfoFilter(BaseModel):

    doc_name: Optional[str] = Field(default=None)
    doc_path: Optional[str] = Field(default=None)
    orientation: Optional[OrderBy] = Field(default=None)
    page: int = Field(default=1)
    order_by: Optional[Orientation] = Field(default=None)

class DocumentInfoMapper():

    def map_in(self, document: DocumentInfoUpdate | DocumentInfo):
        return DocumentInfoSqlModel(
            doc_id=document.doc_id,
            doc_name=document.doc_name,
            doc_path=document.doc_path,
            doc_description=document.doc_description
        )

    def map_out(self, document: DocumentInfoSqlModel | list[DocumentInfoSqlModel]):

        return DocumentInfoOut(
            doc_id=document.doc_id,
            doc_name=document.doc_name,
            doc_path=document.doc_path,
            doc_description=document.doc_description
        )