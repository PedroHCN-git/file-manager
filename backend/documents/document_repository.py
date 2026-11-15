from backend.infra import Session
from backend.documents.document_model import DocumentInfoSqlModel
from backend.documents.document_mapper import DocumentInfoFilter

from sqlalchemy import select

from typing import Optional


class DocumentRepository:

    def save(self, new_doc_info: DocumentInfoSqlModel):

        with Session() as s:

            doc_info = new_doc_info
            old_doc_info = s.get(DocumentInfoSqlModel, new_doc_info.doc_id)

            if old_doc_info:
                old_doc_info.doc_path = new_doc_info.doc_path or old_doc_info.doc_path
                old_doc_info.doc_name = new_doc_info.doc_name or old_doc_info.doc_name
                old_doc_info.doc_description = new_doc_info.doc_description or old_doc_info.doc_description

                doc_info = old_doc_info

            s.add(doc_info)
            s.commit()

    def get_all(
            self,
            doc_filter: Optional[DocumentInfoFilter] = None,
            per_page: int = 20
        ):
        with Session() as s:

            stmt = None

            if doc_filter:
                offset_value = (doc_filter.page - 1) * 20
                stmt = select(
                    DocumentInfoSqlModel
                ).limit(per_page).offset(offset_value)

                if doc_filter.doc_name:
                    stmt = stmt.where(
                        DocumentInfoSqlModel.doc_name.like(f'%{doc_filter.doc_name}%').asc()
                    )

                if doc_filter.doc_path:
                    stmt = stmt.where(
                        DocumentInfoSqlModel.doc_name.like(f'%{doc_filter.doc_path}%').asc()
                    )

                if doc_filter.order_by:
                    stmt = stmt.order_by(doc_filter.order_by)

            if stmt:
                return s.scalars(stmt).all()

            return None

    def get_one(self, doc_id: int):
        with Session() as s:
            result = s.get(DocumentInfoSqlModel, doc_id)

        return result

    def delete(self, doc_id: int):
        with Session.begin() as s:
            document = s.get(DocumentInfoSqlModel, doc_id)
            if document is not None:
                s.delete(document)