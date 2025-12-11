from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.core.engine import get_session
from app.models.order import Order
from app.schemas.order import OrderRead
from app.routes.users import fastapi_users
from app.models.users import User
from typing import List
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/order", tags=["Order"])

@router.get("", response_model=List[OrderRead])
def get_orders(
    current_user: User = Depends(fastapi_users.current_user()),
    session: Session = Depends(get_session)
):
    try:
        result = session.execute(
            select(Order)
            .options(selectinload(Order.items))  # <-- eagerly load items
            .where(Order.owner_id == current_user.id)
        )
        orders = result.scalars().all()
        return orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

