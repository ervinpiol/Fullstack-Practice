from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_async_session
from app.models.users import User
from app.models.order import Order, OrderItem
from app.routes.users import fastapi_users
from app.models.cart import CartItem
from typing import List

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("")
async def checkout(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    # Get all cart items
    result = await session.execute(
        select(CartItem).where(CartItem.owner_id == str(current_user.id))
    )
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate total price
    total_price = 0
    for item in cart_items:
        product = item.product
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
        total_price += product.price * item.quantity

    # Create order header
    new_order = Order(owner_id=str(current_user.id), status="pending", total_price=total_price)
    session.add(new_order)
    await session.flush()  # ensures new_order.id exists

    # Create order items and deduct stock
    for item in cart_items:
        product = item.product
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            total_price=product.price * item.quantity
        )
        session.add(order_item)

        # Deduct stock
        product.stock -= item.quantity
        if product.stock <= 0:
            product.is_active = False
        session.add(product)

        # Remove item from cart
        await session.delete(item)

    await session.commit()
    return {"success": True, "message": "Checkout successful!"}
