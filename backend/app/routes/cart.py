from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.product import Product
from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate, CartItemRead, CartItemUpdate
from app.routes.users import fastapi_users
from app.models.users import User
from typing import List

router = APIRouter(prefix="/cart/items", tags=["Cart"])

@router.get("", response_model=List[CartItemRead])
async def get_cart_items(
    current_user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(CartItem)
            .where(CartItem.owner_id == str(current_user.id))
        )
        items = result.scalars().all()
        return items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


@router.post("", response_model=CartItemRead)
async def add_to_cart(
    item: CartItemCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    try:
        # Check product
        result = await session.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = result.scalars().first()

        if not product:
            raise HTTPException(404, "Product not found")

        if product.stock < item.quantity:
            raise HTTPException(400, "Not enough stock")

        # Check existing cart item for this owner
        result = await session.execute(
            select(CartItem)
            .where(CartItem.product_id == item.product_id)
            .where(CartItem.owner_id == str(current_user.id))
        )
        existing_item = result.scalars().first()

        if existing_item:
            existing_item.quantity += item.quantity
            session.add(existing_item)
        else:
            # existing_item = CartItem(...)
            existing_item = CartItem(
                owner_id=str(current_user.id),
                product_id=item.product_id,
                quantity=item.quantity
            )
            session.add(existing_item)
        
        # Commit
        await session.commit()
        await session.refresh(existing_item)

        return existing_item

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/{cart_item_id}", response_model=CartItemRead)
async def update_quantity(
    cart_item_id: str,
    item: CartItemUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    """
    Update the quantity of a cart item for the current user
    and adjust the product stock accordingly.
    """
    try:
        # Get cart item
        result = await session.execute(
            select(CartItem)
            .where(CartItem.id == cart_item_id)
            .where(CartItem.owner_id == str(current_user.id))
        )
        cart_item = result.scalars().first()

        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        # Verify the product matches
        if cart_item.product_id != item.product_id:
            raise HTTPException(status_code=400, detail="Product ID mismatch")

        # Get product
        result = await session.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = result.scalars().first()

        if not product:
            raise HTTPException(404, "Product not found")
        
        # Calculate stock change
        quantity_change = item.quantity - cart_item.quantity

        if product.stock < quantity_change:
            raise HTTPException(status_code=400, detail="Not enough stock")
        
        # Update cart and product
        cart_item.quantity = item.quantity
        product.stock -= quantity_change
        if product.stock <= 0:
            product.is_active = False

        session.add(cart_item)
        session.add(product)
        await session.commit()
        await session.refresh(cart_item, attribute_names=["product"])

        return cart_item

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{cart_item_id}")
async def remove_product(
    cart_item_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user())
):
    """
    Remove a cart item for the current user
    and optionally restore the product stock.
    """
    try:
        # Get cart item
        result = await session.execute(
            select(CartItem)
            .where(CartItem.id == cart_item_id)
            .where(CartItem.owner_id == str(current_user.id))
        )
        cart_item = result.scalars().first()

        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        # Get the product to restore stock
        result = await session.execute(
            select(Product).where(Product.id == cart_item.product_id)
        )

        # Remove item from the cart
        await session.delete(cart_item)
        await session.commit()

        return {"success": True, "message": "Product successfully removed from the cart"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    