from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from backend.auth.auth_dependency import get_auth_service
from backend.auth.auth_service import AuthService

auth_route = APIRouter(prefix="/auth")
bearer_scheme = HTTPBearer(auto_error=False)


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 43200


@auth_route.post("/login", response_model=TokenOut)
def login(
    credentials: LoginIn,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenOut:
    token = auth_service.login(
        email=credentials.email,
        password=credentials.password,
    )
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenOut(access_token=token)


@auth_route.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    auth_service.logout(token=credentials.credentials)
