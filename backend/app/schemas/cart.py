from pydantic import BaseModel, Field

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)

class CartItemUpdate(BaseModel):
    product_id: int
    quantity: int

class ProductInCart(BaseModel):
    id: int
    name: str
    price: float
    image: str | None = None

    class Config:
        from_attributes = True


class CartItemRead(BaseModel):
    id: int
    product: ProductInCart
    quantity: int

    class Config:
        from_attributes = True