from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import desc
from src.db.model import Product,Category
from .schema import ProductCreate,ProductUpdate,ProductResponse
from typing import List
import uuid
from sqlalchemy.orm import selectinload
from src.catogery.service import CategoryService
from src.error import CategoryNotFound
import logging
Categor_Service=CategoryService()

class ProductService:
    async def create_product(
    self,
    seller_id: uuid.UUID,
    product_data: ProductCreate,
    session: AsyncSession
) -> Product:
    
        try:
          category_product=await Categor_Service.get_category_with_id(product_data.category_id,session)
          if not category_product:
              raise CategoryNotFound()
          new_product = Product(
            product_name=product_data.product_name,
            mrp=product_data.mrp,
            stock=product_data.stock,
            brand=product_data.brand,
            seller_id=seller_id,  
            category_id=product_data.category_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
          new_product.category=category_product
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                detail='Ooops......something went wrong!',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        session.add(new_product)
        await session.commit()
        return new_product
    

    async def get_all_product(self, session: AsyncSession):
        statement = (
            select(Product).order_by(desc(Product.created_at))
        )
        result = await session.execute(statement)
        return result.scalars().all()



    async def get_product(self, product_id: UUID, session: AsyncSession) -> Product:
        result = await session.execute(select(Product).where(Product.uid == product_id).order_by(Product.created_at))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    
    
    async def update_product(
        self,
        product_id: UUID,
        seller_id: UUID,
        product_data: ProductUpdate,
        session: AsyncSession
    ) -> Product:

        # 🔎 نجيب المنتج
        result = await session.execute(
            select(Product).where(Product.uid == product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

  
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403, detail="Not authorized")

   
        update_data = product_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        product.updated_at = datetime.utcnow()

        session.add(product)
        await session.commit()
        await session.refresh(product)
    

    async def delete_product(self, product_id: UUID, seller_id: UUID, session: AsyncSession):
        product = await self.get_product(product_id, session)
        if product.seller_id != seller_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this product")
        await session.delete(product)
        await session.commit()
        return {"message": "Product deleted successfully"}
    
   
    


    async def get_products_by_category(
            self,
        db: AsyncSession, category_id: uuid.UUID
    ) -> List[ProductResponse]:
        """
        Get all products related to a specific category_id
        """
        # Query products filtered by category_id
        result = await db.execute(
            select(Product).where(Product.category_id == category_id)
        )
        products = result.scalars().all()
        
        # Convert to Pydantic response models
        return [ProductResponse.from_orm(product) for product in products]