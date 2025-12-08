from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class CartItem(Base):
    __tablename__ = "cart_item"
    __table_args__ = (UniqueConstraint("owner_id", "product_id", name="unique_cart_item_per_user"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    product = relationship("Product", lazy="joined") 
