from backend.shared import BaseSqlModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR

class DocumentInfoSqlModel(BaseSqlModel):

    __tablename__ = 'documents'

    doc_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doc_name: Mapped[str] = mapped_column(VARCHAR[80])
    doc_path: Mapped[str] = mapped_column(VARCHAR[120])
    doc_description: Mapped[str] = mapped_column(VARCHAR[120])