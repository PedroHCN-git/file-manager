from backend.infra import Session
from backend.documents.document_model import DocumentSqlModel

class DocumentRepository:

    def save(self, document: DocumentSqlModel):

        with Session() as s:
            s.add(document)
            s.commit()

    def get(self, doc_id: int):
        with Session() as s:
            return s.get(DocumentSqlModel, doc_id)

    def delete(self, doc_id: int):
        with Session.begin() as s:
            document = s.get(DocumentSqlModel, doc_id)
            if document is not None:
                s.delete(document)