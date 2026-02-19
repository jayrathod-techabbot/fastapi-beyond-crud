from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


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


class AccountNotVerified(BooklyException):
    """Account is not verified"""

    pass


class PasswordMismatch(BooklyException):
    """Password does not match"""

    pass


def create_exception_handler(
    status_code: int, inital_details: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content=inital_details)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            inital_details={
                "message": "User with email already exists",
                "error_code": "USER_ALREADY_EXISTS",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={
                "message": "Invalid credentials",
                "error_code": "INVALID_CREDENTIALS",
            },
        ),
    )

    app.add_exception_handler(
        TokenExpired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={"message": "Token expired", "error_code": "TOKEN_EXPIRED"},
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={"message": "Token revoked", "error_code": "REVOKED_TOKEN"},
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={"message": "Invalid token", "error_code": "INVALID_TOKEN"},
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={
                "message": "Access token is required",
                "error_code": "ACCESS_TOKEN_REQUIRED",
                "resolution": "Please provide access token",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={
                "message": "Refresh token is required",
                "error_code": "REFRESH_TOKEN_REQUIRED",
                "resolution": "Please provide refresh token",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={
                "message": "Insufficient permission",
                "error_code": "INSUFFICIENT_PERMISSION",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            inital_details={
                "message": "Book not found",
                "error_code": "BOOK_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            inital_details={
                "message": "Review not found",
                "error_code": "REVIEW_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            inital_details={
                "message": "User not found",
                "error_code": "USER_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            inital_details={
                "message": "Account is not verified yet",
                "error_code": "ACCOUNT_NOT_VERIFIED",
                "resolution": "Please verify your account",
            },
        ),
    )

    app.add_exception_handler(
        PasswordMismatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            inital_details={
                "message": "Password & confirm password does not match",
                "error_code": "PASSWORD_MISMATCH",
            },
        ),
    )

    @app.exception_handler(500)
    async def server_error(request: Request, exc: Exception):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "SERVER_ERROR",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
