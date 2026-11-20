import hashlib
import secrets
from datetime import datetime, timedelta

from backend.auth.auth_repository import AuthRepository
from backend.users.password import verify_password
from backend.users.user_model import UserSqlModel
from backend.users.user_repository import UserRepository

SESSION_DURATION = timedelta(hours=12)


class AuthService:

    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository,
    ):
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    def login(self, email: str, password: str) -> str | None:
        user = self.user_repository.get_by_email(email=email)
        if user is None or not verify_password(password, user.password):
            return None

        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self.auth_repository.save_session(
            token_hash=token_hash,
            user_id=user.user_id,
            expires_at=datetime.utcnow() + SESSION_DURATION,
        )
        return token

    def get_user_for_token(self, token: str) -> UserSqlModel | None:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        auth_session = self.auth_repository.get_session(token_hash)
        if auth_session is None:
            return None
        return self.user_repository.get(user_id=auth_session.user_id)

    def logout(self, token: str) -> None:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self.auth_repository.delete_session(token_hash=token_hash)
