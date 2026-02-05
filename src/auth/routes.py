from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.schemas import UserCreateModel, UserResponseModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()


@auth_router.get("/")
async def get_current_user(session: AsyncSession = Depends(get_session)):
    return {"user": "jay"}


@auth_router.post(
    "/signup", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already exists"
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user


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
                user_data={"email": user.email, "uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "uid": str(user.uid)},
                expiry=timedelta(days=7),
                refresh=True,
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email or password is not valid",
        )
