from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.routes.users import fastapi_users
from app.models.users import User
from typing import List

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("", response_model=List[ProductRead])
async def get_products(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    
@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    """
    Create a new product and assign it to the current user
    """
    try:
        product_data = product_in.model_dump(exclude_unset=True) 
        new_product = Product(**product_data, owner_id=str(current_user.id))

        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)

        return new_product
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@router.patch("/{product_id}")
async def update_product(
    product_id: str,
    product_in: ProductUpdate = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Partially update a product by ID
    """
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update fields if provided
        update_data = product_in.model_dump(exclude_unset=True)  # only fields that were provided
        for key, value in update_data.items():
            setattr(product, key, value)

        # Commit changes
        session.add(product)
        await session.commit()
        await session.refresh(product)

        return product
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        await session.delete(product)
        await session.commit()

        return {"success": True, "message": "Product successfully deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
