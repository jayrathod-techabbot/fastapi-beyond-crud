from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import (
    create_exception_handler,
    InvalidToken,
    RevokedToken,
    TokenExpired,
    AccessTokenRequired,
    RefreshTokenRequired,
    UserAlreadyExists,
    InvalidCredentials,
    InsufficientPermission,
    BookNotFound,
    ReviewNotFound,
    UserNotFound,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is started ...")
    await init_db()
    yield
    print("Server is stopped ...")


version = "v1"

app = FastAPI(title="Book API", description="Book API Description", version=version)

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


@app.exception_handler(500)
async def server_error(request: Request, exc: Exception):
    return JSONResponse(
        content={"message": "Oops! Something went wrong","error_code":"SERVER_ERROR"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
