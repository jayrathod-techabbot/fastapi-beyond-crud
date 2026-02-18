from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.db.models import Book
from src.reviews.schema import ReviewModel


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserResponseModel(BaseModel):  # ~ UserModel
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserBooksModel(UserResponseModel):
    books: List[Book]
    reviews: List[ReviewModel]


class EmailModel(BaseModel):
    addresses: List[str]
