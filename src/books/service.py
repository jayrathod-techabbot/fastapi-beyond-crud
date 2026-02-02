from sqlmodel import select,desc
from .models import Book
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import BookCreate,BookUpdate
from datetime import datetime

class BookService:
    async def get_all_books(self,session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_book_by_id(self,book_id: str,session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None  else None

    async def create_book(self,book_data: BookCreate,session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strptime(book_data_dict["published_date"], "%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self,book_id: str,book_data: BookUpdate,session: AsyncSession):
        book_to_update = await self.get_book_by_id(book_id,session)
        if book_to_update:
            update_data_dict = book_data.model_dump(exclude_unset=True)
            for key,value in update_data_dict.items():
                setattr(book_to_update,key,value)
            session.add(book_to_update)
            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        return None

    async def delete_book(self,book_id: str,session: AsyncSession):
        book_to_delete = await self.get_book_by_id(book_id,session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        return None

book_service = BookService()