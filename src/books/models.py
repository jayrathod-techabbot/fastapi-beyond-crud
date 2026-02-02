from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from datetime import datetime,date
import uuid

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
   created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
   update_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

   def __repr__(self):
      return f"<Book {self.title}>"