from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.core.engine import get_session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.routes.users import fastapi_users
from app.models.users import User
from typing import List

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("", response_model=List[ProductRead])
def get_products(session: Session = Depends(get_session)):
    try:
        result = session.execute(select(Product))
        products = result.scalars().all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    try:
        result = session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    
@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user()),
):
    """
    Create a new product and assign it to the current user
    """
    try:
        product_data = product_in.model_dump(exclude_unset=True) 
        new_product = Product(**product_data, owner_id=current_user.id)

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@router.patch("/{product_id}")
def update_product(
    product_id: int,
    product_in: ProductUpdate = Body(...),
    session: Session = Depends(get_session)
):
    """
    Partially update a product by ID
    """
    try:
        result = session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update fields if provided
        update_data = product_in.model_dump(exclude_unset=True)  # only fields that were provided
        for key, value in update_data.items():
            setattr(product, key, value)

        # Commit changes
        session.add(product)
        session.commit()
        session.refresh(product)

        return product
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    try:
        result = session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        session.delete(product)
        session.commit()

        return {"success": True, "message": "Product successfully deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
