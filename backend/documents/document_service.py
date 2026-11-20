from backend.documents.document_mapper import (
    DocumentInfoMapper,
    DocumentInfo,
    DocumentInfoOut,
    DocumentInfoFilter,
    DocumentInfoUpdate
)
from backend.documents.document_repository import DocumentRepository
from fastapi import UploadFile

from typing import Optional
from pathlib import Path
import uuid
import shutil

class DocumentService():

    UPLOAD_DIR = Path(__file__).parent.parent / "upload"

    def __init__(self, repository: DocumentRepository):
        self.mapper = DocumentInfoMapper()
        self.repository = repository

    def save_info(self, document: DocumentInfo | DocumentInfoUpdate):
        sql_model = self.mapper.map_in(document=document)
        return self.repository.save(sql_model)

    def save_many(
        self,
        documents: list[DocumentIn],
        owner_user_id: int,
    ) -> list[DocumentOut]:
        sql_models = [
            self.mapper.map_in(
                document=document,
                owner_user_id=owner_user_id,
            )
            for document in documents
        ]
        saved_documents = self.repository.save_many(sql_models)
        return [
            self.mapper.map_out(document)
            for document in saved_documents
        ]

    def get_all(
            self,
            doc_filter: Optional[DocumentInfoFilter] = DocumentInfoFilter()
        ) -> list[DocumentInfoOut]:
        result = self.repository.get_all(doc_filter=doc_filter)

        return [self.mapper.map_out(line) for line in result]

    def get_one(self, doc_id: int):
        return self.repository.get_one(doc_id=doc_id)

    def upload_file(
            self,
            doc_description: str,
            file: UploadFile,
            doc_id: Optional[int] = None,
        ):

        file_path = None
        
        if doc_id:
            file_path = self.get_one(doc_id=doc_id).doc_path
        else:
            file_path =  self.UPLOAD_DIR / f'{uuid.uuid3(uuid.NAMESPACE_X500, file.filename).int}.{file.filename.split('.')[-1]}'
        

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        self.save_info(
            DocumentInfo(
                doc_id=doc_id,
                doc_name=file.filename,
                doc_path=str(file_path),
                doc_description=doc_description
            )
        )
