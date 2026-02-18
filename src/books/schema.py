from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
import uuid
from src.reviews.schema import ReviewModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class BookDetailModel(Book):
    reviews: List[ReviewModel]


class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[date] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
