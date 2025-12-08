from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base
import uuid

class CartItem(Base):
    __tablename__ = "cart_item"
    __table_args__ = (UniqueConstraint("owner_id", "product_id", name="unique_cart_item_per_user"),)


    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("user.id"), nullable=False)
    product_id = Column(String, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    product = relationship("Product", lazy="joined") 
