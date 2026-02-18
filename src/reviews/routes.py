from fastapi import APIRouter, Depends
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.dependencies import get_current_user
from src.auth.schemas import UserResponseModel
from src.reviews.schema import ReviewCreateModel
from src.reviews.service import ReviewService

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/{book_id}")
async def add_review_to_book(
    book_id: str,
    review_data: ReviewCreateModel,
    curr_user: UserResponseModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):  
    new_review = await review_service.add_review_to_book(
        user_email=curr_user.email,
        book_id=book_id,
        review_data=review_data,
        session=session,
    )
    return new_review
