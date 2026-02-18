from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BooklyException(Exception):
    """Base class"""

    pass


class InvalidToken(BooklyException):
    """Token is invalid"""

    pass


class RevokedToken(BooklyException):
    """Token is revoked"""

    pass


class TokenExpired(BooklyException):
    """Token is expired"""

    pass


class AccessTokenRequired(BooklyException):
    """Access token is required"""

    pass


class RefreshTokenRequired(BooklyException):
    """Refresh token is required"""

    pass


class UserAlreadyExists(BooklyException):
    """User has provided email id which already exists"""

    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password"""

    pass


class InsufficientPermission(BooklyException):
    """User does not have permission to perform the action"""

    pass


class BookNotFound(BooklyException):
    """Book is not found"""
    pass


class ReviewNotFound(BooklyException):
    """Review is not found"""

    pass


class UserNotFound(BooklyException):
    """User is not found"""

    pass


def create_exception_handler(
    status_code: int, inital_details: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content=inital_details)

    return exception_handler
