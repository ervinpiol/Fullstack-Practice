from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
import uuid

class Todo(Base):
    __tablename__ = "todo"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    owner_id = Column(String, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="todos")

