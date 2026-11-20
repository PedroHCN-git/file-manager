from backend.documents.document_mapper import (
    DocumentMapper,
    DocumentIn,
    DocumentOut,
)
from backend.documents.document_repository import DocumentRepository
from backend.documents.document_storage import remove_stored_upload

class DocumentService():

    def __init__(self, repository: DocumentRepository):
        self.mapper = DocumentMapper()
        self.repository = repository

    def save(self, document: DocumentIn, owner_user_id: int) -> DocumentOut:
        sql_model = self.mapper.map_in(
            document=document,
            owner_user_id=owner_user_id,
        )
        saved_document = self.repository.save(sql_model)
        return self.mapper.map_out(saved_document)

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

    def delete(self, doc_id: int, owner_user_id: int) -> bool:
        doc_path = self.repository.delete(
            doc_id=doc_id,
            owner_user_id=owner_user_id,
        )
        if doc_path is None:
            return False
        remove_stored_upload(doc_path)
        return True

    def get(self, doc_id: int, category: str) -> DocumentOut | None:
        result = self.repository.get(doc_id=doc_id, category=category)
        return self.mapper.map_out(result) if result is not None else None

    def get_for_download(
        self,
        doc_id: int,
        category: str,
    ) -> tuple[DocumentOut, str] | None:
        result = self.repository.get(doc_id=doc_id, category=category)
        if result is None:
            return None
        return self.mapper.map_out(result), result.doc_path

    def get_all(
        self,
        category: str,
        name: str | None = None,
    ) -> list[DocumentOut]:
        documents = self.repository.get_all(category=category, name=name)
        return [self.mapper.map_out(document) for document in documents]
