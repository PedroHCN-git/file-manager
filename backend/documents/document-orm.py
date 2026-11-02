from ..shared import BaseOrm

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR

class DocumentOrm(BaseOrm):

    doc_id: Mapped[int] = mapped_column(primary_key=True)
    doc_name: Mapped[str] = mapped_column(VARCHAR[80])
    doc_path: Mapped[str] = mapped_column(VARCHAR[120])