from fastapi import FastAPI, Header, Request  , status 
from typing import Optional 
from datetime import date, datetime
from fastapi.exceptions import HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World !"}

@app.get("/greet")
def read_name(name: Optional[str] = "User", age: Optional[int] = 0) -> dict:
    return {"message" : f"Hello World {name}" , "age" : age}
 

@app.post("/create_book",status_code=status.HTTP_201_CREATED)
def create_book(book: dict) -> dict:
    return {"message" : "Book created successfully"}

@app.get("/get_headers")
async def get_headers(request: Request) -> dict:
    return dict(request.headers)


from pydantic import BaseModel

class Book(BaseModel):
   id : int
   title: str
   author: str
   publisher: str
   published_date: date
   page_count: int
   language: str
   created_at: Optional[date] = None
   update_at: Optional[date] = None

books = [
    {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
        "publisher": "Publisher 1",
        "published_date": "2022-01-01",
        "page_count": 100,
        "language": "English",
        "created_at": "2022-01-01",
        "update_at": "2022-01-01"
    },
    {
        "id": 2,
        "title": "Book 2",
        "author": "Author 2",
        "publisher": "Publisher 2",
        "published_date": "2022-01-01",
        "page_count": 200,
        "language": "English",
        "created_at": "2022-01-01",
        "update_at": "2022-01-01"
    },
    {
        "id": 3,
        "title": "Book 3",
        "author": "Author 3",
        "publisher": "Publisher 3",
        "published_date": "2022-01-01",
        "page_count": 300,
        "language": "English",
        "created_at": "2022-01-01",
        "update_at": "2022-01-01"
    }
]


@app.get("/books",response_model= list[Book])
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int)-> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

@app.post("/books",response_model= Book,status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    new_book = book.dict()
    new_book["created_at"] = date.today()
    new_book["update_at"] = date.today()
    books.append(new_book)
    return new_book