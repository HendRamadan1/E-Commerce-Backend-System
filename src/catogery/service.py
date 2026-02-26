from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import desc
from src.db.model import Category
from .schema import CategoryCreate,CategoryBase,CategoryUpdate
import uuid
from src.error import CategoryNotFound

class CategoryService:
    
    async def create_category(self,session: AsyncSession, data: CategoryCreate):
        category = Category(
            Category_Name=data.Category_Name,
            Description=data.Description
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    

    async def get_all_category(self,session:AsyncSession):
         statement=select(Category).order_by(desc(Category.created_at))
         result=await session.execute(statement)
         return result.scalars().all()
    
    

    async def get_category_with_id(self, category_id: uuid.UUID, session: AsyncSession) -> Category:
        statement =select(Category).where(Category.uid == category_id).order_by(desc(Category.created_at))
        result = await session.execute(statement)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Category not found")
        return product
    
    
    async def update_category(self,session: AsyncSession, category_id: uuid.UUID, data: CategoryUpdate):
        category = await session.get(Category, category_id)
        if not category:
           raise CategoryNotFound()

        if data.Category_Name:
            category.Category_Name = data.Category_Name
        if data.Description:
            category.Description = data.Description

        category.updated_at = datetime.utcnow()

        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    
    

    async def delete_category(self,session: AsyncSession, category_id: uuid.UUID):
        category = await session.get(Category, category_id)
        if not category:
            raise CategoryNotFound()

        await session.delete(category)
        await session.commit()
        return True
    
    
    

    



