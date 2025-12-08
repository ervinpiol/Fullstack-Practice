from pydantic import BaseModel
from typing import List, Optional

class OrderItemRead(BaseModel):
    id: str
    product_id: str
    quantity: int
    total_price: float

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: str
    owner_id: str
    status: str
    total_price: float
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    items: List[OrderItemRead]  # list of items in the order
    status: Optional[str] = "pending"
    total_price: Optional[float] = 0.0

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_price: Optional[float] = None
