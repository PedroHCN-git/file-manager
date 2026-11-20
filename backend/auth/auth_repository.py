from datetime import datetime

from backend.auth.auth_model import AuthSessionSqlModel
from backend.infra import Session


class AuthRepository:

    def save_session(
        self,
        token_hash: str,
        user_id: int,
        expires_at: datetime,
    ) -> None:
        with Session.begin() as session:
            session.add(
                AuthSessionSqlModel(
                    token_hash=token_hash,
                    user_id=user_id,
                    expires_at=expires_at,
                )
            )

    def get_session(self, token_hash: str) -> AuthSessionSqlModel | None:
        with Session() as session:
            auth_session = session.get(AuthSessionSqlModel, token_hash)
            if (
                auth_session is None
                or auth_session.expires_at <= datetime.utcnow()
            ):
                return None
            return auth_session

    def delete_session(self, token_hash: str) -> None:
        with Session.begin() as session:
            auth_session = session.get(AuthSessionSqlModel, token_hash)
            if auth_session is not None:
                session.delete(auth_session)
