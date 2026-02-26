from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException,Body
from fastapi import APIRouter,status,Depends
from typing import Optional,List
from .schema import ProductCreate ,ProductResponse,ProductUpdate
from .service import ProductService
from src.db.main import get_session
from src.db.model import Customer
from src.auth.dependence import get_current_user,RoleCheck
from src.seller.depemdence import check_product_owner,require_seller
from src.product.dependence import get_current_seller_id
import uuid
product_router=APIRouter()
product_service=ProductService()



@product_router.get('/',response_model=List[ProductResponse])
async def get_all_products(
    session:AsyncSession=Depends(get_session),

):
    products =await product_service.get_all_product(session=session)
    return products


   
    

@product_router.get('/{product_id}',response_model=ProductResponse)
async def get_product(
    product_id,
    session:AsyncSession=Depends(get_session),

)->dict:
    product=await product_service.get_product(product_id,session)
    if product:
     return product
    else :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)




@product_router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate , # validation body happens first
    seller_id: uuid.UUID = Depends(get_current_seller_id),
    _: bool = Depends(RoleCheck(["seller"])),  # role check happens after body validation
    session: AsyncSession = Depends(get_session)
):
    """
    Seller creates a new product.
    """
    new_product = await product_service.create_product(
        seller_id=seller_id,
        product_data=product_data,
        session=session
    )
    return new_product




@product_router.patch("/update/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_session),
    seller_uid: Customer = Depends(get_current_seller_id)
):



    updated_product = await product_service.update_product(
        product_id=product_id,
        seller_id=seller_uid,
        product_data=product_data,
        session=session
    )

    return updated_product
   


@product_router.delete('/delete/{product_id}',status_code=status.HTTP_201_CREATED)
async def delete_product(product_id:str,session:AsyncSession=Depends(get_session),product=Depends(check_product_owner),seller_uid:Customer=Depends(get_current_seller_id))->dict:
   delete_product=await product_service.delete_product(product_id,seller_uid,session=session)
   if delete_product is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   else:
      return delete_product

