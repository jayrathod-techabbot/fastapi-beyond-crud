from sqlmodel import SQLModel,Field,Column , Relationship
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from datetime import datetime,date
import uuid
from src.auth.models import User

class Book(SQLModel, table=True):
   __tablename__ = "books"

   uid : uuid.UUID = Field(
    sa_column=Column(
      pg.UUID,
      primary_key=True,
      nullable=False,
      default=uuid.uuid4
    )
   )
   title: str
   author: str
   publisher: str
   published_date: date
   page_count: int
   language: str
   user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
   created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
   update_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

   user: Optional[User] = Relationship(back_populates="books")
   
   def __repr__(self):
      return f"<Book {self.title}>"