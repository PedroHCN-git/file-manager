from backend.infra import Session
from backend.documents.document_model import DocumentSqlModel
from backend.users.user_model import UserSqlModel
from sqlalchemy import select

class DocumentRepository:

    def save(self, document: DocumentSqlModel) -> DocumentSqlModel:
        with Session() as s:
            s.add(document)
            s.commit()
            s.refresh(document)
            return document

    def save_many(
        self,
        documents: list[DocumentSqlModel],
    ) -> list[DocumentSqlModel]:
        with Session() as session:
            session.add_all(documents)
            session.commit()
            for document in documents:
                session.refresh(document)
            return documents

    def get(self, doc_id: int, category: str) -> DocumentSqlModel | None:
        with Session() as s:
            return s.scalar(
                select(DocumentSqlModel)
                .join(
                    UserSqlModel,
                    DocumentSqlModel.owner_user_id == UserSqlModel.user_id,
                )
                .where(
                    DocumentSqlModel.doc_id == doc_id,
                    UserSqlModel.category == category,
                )
            )

    def get_all(
        self,
        category: str,
        name: str | None = None,
    ) -> list[DocumentSqlModel]:
        with Session() as s:
            statement = (
                select(DocumentSqlModel)
                .join(
                    UserSqlModel,
                    DocumentSqlModel.owner_user_id == UserSqlModel.user_id,
                )
                .where(UserSqlModel.category == category)
            )
            search_term = (name or "").strip()
            if search_term:
                escaped_term = (
                    search_term.replace("\\", "\\\\")
                    .replace("%", "\\%")
                    .replace("_", "\\_")
                )
                statement = statement.where(
                    DocumentSqlModel.doc_name.ilike(
                        f"%{escaped_term}%",
                        escape="\\",
                    )
                )
            return list(s.scalars(statement).all())

    def delete(self, doc_id: int, owner_user_id: int) -> str | None:
        with Session.begin() as s:
            document = s.scalar(
                select(DocumentSqlModel)
                .where(
                    DocumentSqlModel.doc_id == doc_id,
                    DocumentSqlModel.owner_user_id == owner_user_id,
                )
            )
            if document is None:
                return None
            doc_path = document.doc_path
            s.delete(document)
            return doc_path