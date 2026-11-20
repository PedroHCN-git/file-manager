from backend.shared import BaseSqlModel

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///backend/infra/database.db", echo=True)

Session = sessionmaker(bind=engine)


def create_tables() -> None:
    BaseSqlModel.metadata.create_all(engine)
    columns = {
        column["name"]
        for column in inspect(engine).get_columns("documents")
    }
    if "owner_user_id" not in columns:
        with engine.begin() as connection:
            connection.exec_driver_sql(
                "ALTER TABLE documents "
                "ADD COLUMN owner_user_id INTEGER REFERENCES users(user_id)"
            )