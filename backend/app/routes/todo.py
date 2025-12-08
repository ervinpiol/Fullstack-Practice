from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoRead, TodoUpdate
from typing import Optional
from app.routes.users import fastapi_users
from app.models.users import User

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.get("", response_model=list[TodoRead])
async def get_todos(
    completed: Optional[bool] = None,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    try:
        query = select(Todo).where(Todo.owner_id == current_user.id)

        if completed is not None:
            query = query.where(Todo.completed == completed)

        result = await session.execute(query)
        todos = result.scalars().all()
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    try:
        result = await session.execute(
        select(Todo).where(Todo.id == todo_id, Todo.owner_id == current_user.id)
    )
        todo = result.scalars().first()

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        return todo

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=TodoRead)
async def create_todo(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    try:
        todo_data = todo.model_dump(exclude_unset=True)
        new_todo = Todo(**todo_data, owner_id=current_user.id)

        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)

        return new_todo
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate = Body(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    try:
        result = await session.execute(
            select(Todo).where(Todo.id == todo_id, Todo.owner_id == current_user.id)
        )

        todo = result.scalars().first()

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        update_data = todo_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo, key, value)

        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        return todo

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    try:
        result = await session.execute(
            select(Todo).where(Todo.id == todo_id, Todo.owner_id == current_user.id)
        )

        todo = result.scalars().first()

        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        await session.delete(todo)
        await session.commit()

        return {"success": True, "message": "Todo successfully deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
