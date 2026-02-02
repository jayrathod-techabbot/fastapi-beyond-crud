from fastapi import APIRouter , status , Depends , HTTPException
from .schema import BookUpdate, Book, BookCreate
from src.books.service import BookService
# from .books_data import books
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

book_router = APIRouter()
book_service = BookService()

@book_router.post("/",response_model= Book,status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookCreate, session: AsyncSession = Depends(get_session)): 
    new_book = await book_service.create_book(new_book,session)
    return new_book

@book_router.get("/",response_model= list[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    book = await book_service.get_all_books(session)
    return book

@book_router.get("/{book_id}",response_model=Book)
async def get_book(book_id : str, session: AsyncSession = Depends(get_session))-> dict:
    book = await book_service.get_book_by_id(book_id,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@book_router.patch("/{book_id}",status_code=status.HTTP_201_CREATED,response_model=Book)
async def update_book(book_id : str, book_data: BookUpdate, session: AsyncSession = Depends(get_session))-> dict:
    updated_book = await book_service.update_book(book_id,book_data,session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@book_router.delete("/{book_id}")
async def delete_book(book_id : str, session: AsyncSession = Depends(get_session))-> dict:
    deleted_book = await book_service.delete_book(book_id,session)
    if deleted_book:
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
