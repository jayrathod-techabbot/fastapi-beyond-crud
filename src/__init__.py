from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import register_all_errors
from .middlerware import register_all_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is started ...")
    await init_db()
    yield
    print("Server is stopped ...")


version = "v1"

app = FastAPI(title="Book API", description="Book API Description", version=version)
register_all_errors(app)
register_all_middleware(app)



@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
