from backend.users.user_mapper import UserIn, UserMapper, UserOut
from backend.users.user_repository import UserRepository


class UserService:

    def __init__(self, repository: UserRepository):
        self.mapper = UserMapper()
        self.repository = repository

    def save(self, user: UserIn) -> UserOut:
        saved_user = self.repository.save(self.mapper.map_in(user))
        return self.mapper.map_out(saved_user)

    def get(self, user_id: int) -> UserOut | None:
        user = self.repository.get(user_id=user_id)
        if user is None:
            return None
        return self.mapper.map_out(user)

    def get_all(self) -> list[UserOut]:
        return [
            self.mapper.map_out(user)
            for user in self.repository.get_all()
        ]

    def delete(self, user_id: int) -> bool:
        return self.repository.delete(user_id=user_id)
