from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import Create_Review
from src.auth.service import CustomerServicee
from src.product.service import ProductService
from src.db.model import Review
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import select,desc
import logging
from src.error import productNotFound,UserNotFound

user_service=CustomerServicee()
product_service=ProductService()

class ReviewService:
    async def add_review_product(
            self,
            user_email:str,
            product_uid:str,
            reviews_data:Create_Review,
            session:AsyncSession):
        try:
            product= await product_service.get_product(product_id=product_uid,session=session)
            user=await user_service.get_user(email=user_email,session=session)
            reviews_data_dict=reviews_data.model_dump()
            new_reviews=Review(**reviews_data_dict)
            if not product:
                raise productNotFound()
            
            if not user:
                raise UserNotFound
            
            new_reviews.customer=user
            new_reviews.product=product
            session.add(new_reviews)
            await session.commit()
            return new_reviews
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                detail='Ooops......something went wrong!',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            

    async def get_review(self,review_id:str,session:AsyncSession):
        statement=select(Review).where(Review.uid==review_id)
        result=await session.execute(statement)
        return result.scalars().all()
    



    async def get_all_reviews(self,session:AsyncSession):
         statement=select(Review).order_by(desc(Review.created_at))
         result=await session.execute(statement)
         return result.scalars().all()



    async def delete_review(self,review_id:str,user_email:str,session:AsyncSession):
        user= await user_service.get_user(user_email,session)
        review=await self.get_review(review_id,session)
        if not review or review.user is not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Cannot delete this review')
        session.add(review)
        await session.commit()


    