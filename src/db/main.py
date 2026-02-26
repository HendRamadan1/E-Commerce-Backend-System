from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.Config import config
engine=create_async_engine(
    
        url=config.DATABASE_URL,
        echo=True
    
)


async def init_db():
    async with engine.begin()as conn:
        await conn.run_sync(SQLModel.metadata.create_all)   



async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session()-> AsyncSession:
   
    async with async_session()as session:
        yield session



