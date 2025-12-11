from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.users import User
from app.schemas.users import UserRead
from app.models.users import User
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))