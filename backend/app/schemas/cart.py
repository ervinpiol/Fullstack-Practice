from pydantic import BaseModel, Field

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(1, ge=1)

class CartItemUpdate(BaseModel):
    product_id: str
    quantity: int

class ProductInCart(BaseModel):
    id: str
    name: str
    price: float
    image: str | None = None

    class Config:
        from_attributes = True


class CartItemRead(BaseModel):
    id: str
    product: ProductInCart
    quantity: int

    class Config:
        from_attributes = True