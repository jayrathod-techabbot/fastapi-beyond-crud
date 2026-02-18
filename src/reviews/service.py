from sqlalchemy.ext.asyncio import AsyncSession
from .schema import ReviewCreateModel
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from src.db.main import get_session
import logging
import uuid

logger = logging.getLogger(__name__)

book_service = BookService()
user_service = UserService()


class ReviewService:

    async def add_review_to_book(
        self,
        user_email: str,
        book_id: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        logger.info(f"Adding review to book {book_id} by user {user_email}")

        try:
            book = await book_service.get_book_by_id(book_id=book_id, session=session)
            if book is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
                )

            user = await user_service.get_user_by_email(
                email=user_email, session=session
            )
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            new_review = Review(**review_data.model_dump())

            new_review.book = book
            new_review.user = user
            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            return new_review

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding review: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )
