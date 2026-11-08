from backend.documents.document_mapper import (
    DocumentMapper,
    DocumentIn,
    DocumentOut
)
from backend.documents.document_repository import DocumentRepository

class DocumentService():

    def __init__(self, repository: DocumentRepository):
        self.mapper = DocumentMapper()
        self.repository = repository

    def save(self, document: DocumentIn):
        sql_model = self.mapper.map_in(document=document)
        return self.repository.save(sql_model)

    def delete(self, doc_id: int):
        return self.repository.delete(doc_id=doc_id)

    def get(self, doc_id: int) -> DocumentOut:
        result = self.repository.get(doc_id=doc_id)
        out = self.mapper.map_out(result)
        return out
        

    def get_all(self):
        ...

        


