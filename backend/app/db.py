from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that yields an asynchronous database session."""
    async with async_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Dependency for retrieving the user database adapter.
    User model imported here to break the circular dependency.
    """
    from app.models.users import User 
    yield SQLAlchemyUserDatabase(session, User)