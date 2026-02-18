from src.db.models import User
from .schemas import UserCreateModel
from typing import Optional
# from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import generate_password_hash
from src.db.main import get_session


class UserService:
    async def get_user_by_email(
        self, email: str, session: AsyncSession
    ) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalars().one_or_none()

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.dict()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)
        return new_user
