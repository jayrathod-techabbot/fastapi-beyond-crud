from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.service import UserService
from .models import User
from typing import List, Any

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        crede = await super().__call__(request)

        token = crede.credentials
        token_data = decode_access_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expire",
                    "resolution": "Please get new token",
                },
            )

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token",
                },
            )
        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data: dict) -> dict:
        raise NotImplementedError("Subclasses must implement verify_token_data method")

    def token_valid(self, token):
        token_data = decode_access_token(token)
        return token_data is not None


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> dict:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide access token not refresh token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> dict:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide refresh token not access token",
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> dict:
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(self,curr_user:User = Depends(get_current_user)):
        if curr_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource",
        )

