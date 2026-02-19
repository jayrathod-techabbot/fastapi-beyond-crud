from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.schemas import (
    UserCreateModel,
    UserResponseModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import (
    create_access_token,
    decode_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    generate_password_hash,
)
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist
from src.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
    TokenExpired,
    UserNotFound,
    PasswordMismatch,
)
from src.mail import create_message, mail
from src.config import Config

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses
    html = "<h1> Welcome to the app </h1>"
    message = create_message(recipients=emails, subject="Welcome to the app", body=html)
    await mail.send_message(message)
    return JSONResponse(content={"message": "Email sent successfully"})


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": new_user.email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
                <h1> Welcome to the app </h1>
                <p> Click on the link to verify your email </p>
                <a href="{link}"> Verify Email </a>
                """
    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )
    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "User created successfully. Please verify your account.",
            "user": jsonable_encoder(new_user),
        }
    )


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {"is_verified": True}, session)
        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred while verifying the account"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/login")
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password
    user = await user_service.get_user_by_email(email, session)

    if user:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                expiry=timedelta(days=7),
                refresh=True,
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "user_uid": str(user.uid)},
                }
            )
    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_refresh_token(token_details: dict = Depends(RefreshTokenBearer())):
    expire_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expire_timestamp) < datetime.now():
        raise TokenExpired()

    new_access_token = create_access_token(user_data=token_details["user"])

    return JSONResponse(content={"access_token": new_access_token})


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user: dict = Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    await add_jti_to_blocklist(token_details["jti"])
    return JSONResponse(
        content={
            "message": "Token revoked successfully. Logged out sucessfully",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-request")
async def password_reset_request(
    user_data: PasswordResetRequestModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user = await user_service.get_user_by_email(email, session)
    if not user:
        raise UserNotFound()
    token = create_url_safe_token({"email": user.email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset/{token}"
    html_message = f"""
                <h1> Reset your password </h1>
                <p> Click on the link to reset your password </p>
                <a href="{link}"> Reset Password </a>
                """
    message = create_message(
        recipients=[email], subject="Reset your password", body=html_message
    )
    await mail.send_message(message)
    return JSONResponse(
        content={
            "message": "Password reset link sent successfully",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset/{token}")
async def verify_user_account(
    token: str,
    password_data: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):

    new_password = password_data.new_password
    confirm_password = password_data.comfirm_new_password

    if new_password != confirm_password:
        raise PasswordMismatch()
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()

        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {"password_hash": password_hash}, session)
        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred while resetting the password"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
