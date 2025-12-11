from sqlalchemy.orm import DeclarativeBase
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.engine import get_session

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


def get_user_db(session: Session = Depends(get_session)):
    """
    Dependency for retrieving the user database adapter.
    User model imported here to break the circular dependency.
    """
    from app.models.users import User 
    yield SQLAlchemyUserDatabase(session, User)