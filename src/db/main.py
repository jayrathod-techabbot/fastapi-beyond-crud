from sqlmodel import create_engine , text
from src.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(create_engine(url= Config.DATABASE_URL,echo=True))
# SQLModel.metadata.create_all(engine)


async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book
        
        await conn.run_sync(SQLModel.metadata.create_all)
    
async def get_session():
    Session = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
    async with Session() as session:
        yield session