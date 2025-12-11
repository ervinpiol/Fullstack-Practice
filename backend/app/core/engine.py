import contextlib
import threading
from sqlalchemy import text
from sqlalchemy.engine import create_engine
from typing import ContextManager
from sqlalchemy.engine import Engine
from collections.abc import AsyncGenerator
from collections.abc import Generator
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


SYNC_DB_API = "psycopg2"
ASYNC_DB_API = "asyncpg"
_ASYNC_ENGINE: AsyncEngine | None = None


def build_connection_string(
    db_api: str = ASYNC_DB_API,
    user: str = settings.postgres_user,
    password: str = settings.postgres_password,
    host: str = settings.postgres_host,
    port: str = settings.postgres_port,
    db: str = settings.postgres_db,
) -> str:
    return f"postgresql+{db_api}://{user}:{password}@{host}:{port}/{db}"


def build_connecting_string_supabase(
    db_password: str = settings.postgres_password,
) -> str:
    return f"postgresql://postgres.bzyxwswrtcdatuwyvhmv:{db_password}@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"

class SupabaseEngine:
    _engine: Engine | None = None
    _lock: threading.Lock = threading.Lock()

    @classmethod
    def _init_engine(cls) -> Engine:
        try:
            if not cls._engine:
                conn_string = build_connecting_string_supabase()
                cls._engine = create_engine(conn_string)
        except Exception as e:
            print(f"Error initializing the database engine: {e}")
            raise
        return cls._engine

    @classmethod
    def get_engine(cls) -> Engine:
        """Gets the sql alchemy engine. Will init a default engine if init hasn't
        already been called. You probably want to init first!"""
        try:
            if not cls._engine:
                with cls._lock:
                    if not cls._engine:
                        cls._engine = cls._init_engine()
        except Exception as e:
            print(f"Error getting the database engine: {e}")
            raise
        return cls._engine

def get_session() -> Generator[Session, None, None]:
    with Session(get_sync_engine(), expire_on_commit=False) as session:
        yield session


def get_session_context_manager() -> ContextManager[Session]:
    return contextlib.contextmanager(get_session)()


def get_sync_engine() -> Engine:
    print("Getting sync engine")
    return SupabaseEngine.get_engine()


def get_async_engine() -> AsyncEngine:
    print("Getting async engine")
    global _ASYNC_ENGINE
    if not _ASYNC_ENGINE:
        conn_string = build_connection_string()
        _ASYNC_ENGINE = create_async_engine(
            conn_string,
            pool_size=40,
            max_overflow=10,
        )
    return _ASYNC_ENGINE


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(
        get_async_engine(), expire_on_commit=False
    ) as async_session:
        yield async_session


async def warm_up_connections(
    sync_conn_to_warmup: int = 10, async_conn_to_warmup: int = 10
) -> None:
    print("Warming up database connections...")
    sync_postgres_engine = get_sync_engine()
    connections = [sync_postgres_engine.connect() for _ in range(sync_conn_to_warmup)]
    for conn in connections:
        conn.execute(text("SELECT 1"))
    for conn in connections:
        conn.close()

    # async_postgres_engine = get_async_engine()
    # async_connections = [
    #     await async_postgres_engine.connect() for _ in range(async_conn_to_warmup)
    # ]
    # for async_conn in async_connections:
    #     await async_conn.execute(text("SELECT 1"))
    # for async_conn in async_connections:
    #     await async_conn.close()


def get_session_factory(fresh=False, expire_on_commit=True) -> sessionmaker[Session]:
    global SessionFactory
    if SessionFactory is None or fresh:
        SessionFactory = sessionmaker(
            bind=SupabaseEngine.get_engine(),
            expire_on_commit=expire_on_commit,
        )
    return SessionFactory