from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is started ...")
    await init_db()
    yield
    print("Server is stopped ...")


version = "v1"

app = FastAPI(
    title="Book API",
    description="Book API Description",
    version=version,
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

app.include_router(book_router,prefix=f"/api/{version}/books",tags=["books"])
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=["auth"])







