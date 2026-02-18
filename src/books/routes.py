from fastapi import APIRouter, status, Depends, HTTPException
from .schema import BookUpdate, Book, BookCreate , BookDetailModel
from src.books.service import BookService

# from .books_data import books
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

from src.auth.dependencies import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@book_router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def create_book(
    new_book: BookCreate,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(new_book, user_id, session)
    return new_book


@book_router.get("/", response_model=list[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):

    print(f"USER DETAILS = {token_details}")
    books = await book_service.get_all_books(session)
    return books


@book_router.get(
    "/user/{user_id}", response_model=list[Book], dependencies=[role_checker]
)
async def get_user_book_submissions(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_id, session)
    return books


@book_router.get("/{book_id}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book_by_id(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    book = await book_service.get_book_by_id(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@book_router.patch(
    "/{book_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker],
)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    updated_book = await book_service.update_book(book_id, book_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@book_router.delete("/{book_id}", dependencies=[role_checker])
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    deleted_book = await book_service.delete_book(book_id, session)
    if deleted_book:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
