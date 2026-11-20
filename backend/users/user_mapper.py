from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.users.password import hash_password
from backend.users.user_model import UserSqlModel
from typing import Self


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


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=3, max_length=255)
    password: str | None = Field(default=None, min_length=8)

    @model_validator(mode="after")
    def validate_changes(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Provide at least one account field to update.")
        if self.name is not None and not self.name.strip():
            raise ValueError("Name cannot be blank.")
        if self.email is not None and not self.email.strip():
            raise ValueError("Email cannot be blank.")
        if self.password is not None and not self.password.strip():
            raise ValueError("Password cannot be blank.")
        return self


class UserMapper:

    def map_in(self, user: UserIn) -> UserSqlModel:
        return UserSqlModel(
            name=user.name,
            category=user.category,
            email=user.email,
            password=hash_password(user.password),
        )

    def map_out(self, user: UserSqlModel) -> UserOut:
        return UserOut(
            user_id=user.user_id,
            name=user.name,
            category=user.category,
            email=user.email,
        )
