from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.product import Product
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from app.routes.users import fastapi_users
from app.models.users import User
from typing import List
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/order", tags=["Order"])

@router.get("", response_model=List[OrderRead])
async def get_orders(
    current_user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(Order)
            .options(selectinload(Order.items))  # <-- eagerly load items
            .where(Order.owner_id == str(current_user.id))
        )
        orders = result.scalars().all()
        return orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

