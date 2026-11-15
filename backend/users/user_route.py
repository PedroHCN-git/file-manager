from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend.users.user_mapper import UserIn, UserOut
from backend.users.user_repository import UserRepository
from backend.users.user_service import UserService


user_route = APIRouter(prefix="/users")


def get_repository() -> UserRepository:
    return UserRepository()


def get_service() -> UserService:
    return UserService(repository=get_repository())


@user_route.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def save_user(
    user: UserIn,
    user_service: UserService = Depends(get_service),
) -> UserOut:
    return user_service.save(user=user)


@user_route.get("/", response_model=list[UserOut])
def get_users(
    user_service: UserService = Depends(get_service),
) -> list[UserOut]:
    return user_service.get_all()


@user_route.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    user_service: UserService = Depends(get_service),
) -> UserOut:
    user = user_service.get(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@user_route.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_service),
) -> Response:
    if not user_service.delete(user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
