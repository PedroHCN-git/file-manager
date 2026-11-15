from sqlalchemy import select

from backend.infra import Session
from backend.users.user_model import UserSqlModel


class UserRepository:

    def save(self, user: UserSqlModel) -> UserSqlModel:
        with Session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get(self, user_id: int) -> UserSqlModel | None:
        with Session() as session:
            return session.get(UserSqlModel, user_id)

    def get_all(self) -> list[UserSqlModel]:
        with Session() as session:
            return list(session.scalars(select(UserSqlModel)).all())

    def delete(self, user_id: int) -> bool:
        with Session.begin() as session:
            user = session.get(UserSqlModel, user_id)
            if user is None:
                return False
            session.delete(user)
            return True
