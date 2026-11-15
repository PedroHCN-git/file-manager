import hashlib
import secrets

from pydantic import BaseModel

from backend.users.user_model import UserSqlModel


class UserIn(BaseModel):
    name: str
    category: str
    email: str
    password: str


class UserOut(BaseModel):
    user_id: int
    name: str
    category: str
    email: str


class UserMapper:

    def map_in(self, user: UserIn) -> UserSqlModel:
        salt = secrets.token_bytes(16)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            user.password.encode("utf-8"),
            salt,
            600_000,
        )
        stored_password = f"pbkdf2_sha256${salt.hex()}${password_hash.hex()}"

        return UserSqlModel(
            name=user.name,
            category=user.category,
            email=user.email,
            password=stored_password,
        )

    def map_out(self, user: UserSqlModel) -> UserOut:
        return UserOut(
            user_id=user.user_id,
            name=user.name,
            category=user.category,
            email=user.email,
        )
