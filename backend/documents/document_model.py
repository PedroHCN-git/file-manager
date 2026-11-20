from backend.shared import BaseSqlModel

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

class DocumentSqlModel(BaseSqlModel):

    __tablename__ = "documents"

    doc_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doc_name: Mapped[str] = mapped_column(String(80), nullable=False)
    doc_path: Mapped[str] = mapped_column(String(120), nullable=False)
    doc_description: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="",
    )
    owner_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=True,
    )