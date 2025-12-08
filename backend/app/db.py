from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from app.core.config import settings
from typing import AsyncGenerator

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

engine = create_async_engine(
    settings.SUPABASE_DB_URL,
    echo=True,  # turn off in production
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Dependency for retrieving the user database adapter.
    User model imported here to break the circular dependency.
    """
    from app.models.users import User 
    yield SQLAlchemyUserDatabase(session, User)