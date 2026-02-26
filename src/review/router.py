from fastapi.routing import APIRouter
from src.auth.dependence import RoleCheck,AccessTokenBearer,get_current_user
from fastapi import status , Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.db.model import Customer
from .schema import Create_Review
from src.error import productNotFound
from src.review.service import ReviewService
review_service=ReviewService()
user_role_check=Depends(RoleCheck(['admin','Customer']))
review_router=APIRouter()


@review_router.post('/prodcut/{product_id}',dependencies=[user_role_check])
async def add_reviews_product(product_id:str,reviews_data:Create_Review,user:Customer=Depends(get_current_user),session:AsyncSession=Depends(get_session)):
    new_review=await review_service.add_review_product(user_email=user.Email,product_uid=product_id,reviews_data=reviews_data,session=session)
    return new_review



@review_router.get('/{review_id}',dependencies=[user_role_check])
async def get_review_for_product(review_id:str,session:AsyncSession=Depends(get_session)):
    product=await review_service.get_review(review_id,session)
    if not product :
        raise  productNotFound()
    else:
         return product




@review_router.get('/',dependencies=[user_role_check])
async def get_all_reviews(session:AsyncSession=Depends(get_session)):
    prodcuts=await review_service.get_all_reviews(session)
    return prodcuts





@review_router.delete('/{review_id}',dependencies=[user_role_check])
async def delete_review(
    review_id:str,
    current_user:Customer=Depends(get_current_user),
    session:AsyncSession=Depends(get_session)):
        await review_service.delete_review(review_id,user_email=current_user.Email,session=session)
        return None

