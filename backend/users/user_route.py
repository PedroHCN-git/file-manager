from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from backend.auth.auth_dependency import get_current_user
from backend.users.user_mapper import UserIn, UserOut, UserUpdate
from backend.users.user_model import UserSqlModel
from backend.users.user_repository import UserRepository
from backend.users.user_service import UserService


user_route = APIRouter(prefix="/users")


def get_repository() -> UserRepository:
    return UserRepository()


def get_service() -> UserService:
    return UserService(repository=get_repository())

@user_route.get("/me", response_model=UserOut)
def get_current_user_profile(
    current_user: UserSqlModel = Depends(get_current_user),
    user_service: UserService = Depends(get_service),
) -> UserOut:
    user = user_service.get(user_id=current_user.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@user_route.patch("/me", response_model=UserOut)
def update_current_user_profile(
    changes: UserUpdate,
    current_user: UserSqlModel = Depends(get_current_user),
    user_service: UserService = Depends(get_service),
) -> UserOut:
    try:
        user = user_service.update(
            user_id=current_user.user_id,
            changes=changes,
        )
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from error

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@user_route.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def save_user(
    user: UserIn,
    user_service: UserService = Depends(get_service),
) -> UserOut:
    try:
        return user_service.save(user=user)
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from error


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
