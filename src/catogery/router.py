from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid 
from .dependece import admin_only
from src.error import CategoryNotFound
from src.product.service import ProductService
from src.db.main import get_session
from .schema import (
    CategoryCreate,
    CategoryBase,
    CategoryUpdate,
    

)
from .service import CategoryService
from typing import List
from src.product.schema import ProductResponse
product_service=ProductService()
category_service=CategoryService()

category_router=APIRouter()

# =====================================================
# ✅ Create Category (Admin Only)
# =====================================================


@category_router.post("/", response_model=CategoryBase,dependencies=[Depends(admin_only)],status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(
    data: CategoryCreate,
    session: AsyncSession = Depends(get_session)
):
    return await category_service.create_category(session, data)


# =====================================================
# ✅ Get All Categories
# =====================================================
@category_router.get("/", response_model=list[CategoryBase],dependencies=[Depends(admin_only)])
async def list_categories(session: AsyncSession = Depends(get_session)):
    return await category_service.get_all_category(session)


# =====================================================
# ✅ Get Category by ID
# =====================================================
@category_router.get("/{category_id}", response_model=CategoryBase,dependencies=[Depends(admin_only)])
async def get_category(category_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    category = await category_service.get_category_with_id(category_id, session)
    if not category:
       raise CategoryNotFound()
    return category




# =====================================================
# ✅ Update Category
# =====================================================
@category_router.patch("/{category_id}", response_model=CategoryBase,dependencies=[Depends(admin_only)])
async def update_category_endpoint(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    session: AsyncSession = Depends(get_session)
):
    category = await category_service.update_category(session, category_id, data)
    if not category:
        raise CategoryNotFound()
    return category


# =====================================================
# ✅ Delete Category
# =====================================================
@category_router.delete("/{category_id}",dependencies=[Depends(admin_only)],status_code=status.HTTP_201_CREATED)
async def delete_category_endpoint(
    category_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    success = await category_service.delete_category(session, category_id)
    if not success:
        raise CategoryNotFound()
    return {"message": "Category deleted successfully"}

@category_router.get("/{category_id}/products", response_model=List[ProductResponse])
async def read_products_by_category(
    category_id: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    products = await  product_service.get_products_by_category(session, category_id)
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")
    return products




