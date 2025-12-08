from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    # Todos (owned by the user; safe to delete together)
    todos = relationship(
        "Todo",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # Products (owned/created by the user; should be deleted with the user)
    products = relationship(
        "Product",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # Orders (historical records; NEVER delete this automatically)
    orders = relationship(
        "Order",
        back_populates="owner",
        cascade=None  # default: no cascade
    )
