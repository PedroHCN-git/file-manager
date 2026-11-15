from backend.shared import BaseSqlModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///backend/infra/database.db", echo=True)
BaseSqlModel.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def create_tables() -> None:
    BaseSqlModel.metadata.create_all(engine)