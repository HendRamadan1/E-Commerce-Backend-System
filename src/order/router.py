from fastapi.routing import APIRouter
from src.auth.dependence import RoleCheck
from fastapi import status , Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.db.model import Customer
from .schema import CreateOrder,OrderBase,OrderUpdate
import uuid
from src.error import OrderNotFound
from .service import OrderService
order_service=OrderService()
user_role_check=Depends(RoleCheck(['admin','Customer']))
order_router=APIRouter()



@order_router.post("/{customer_id}/checkout")
async def checkout(
    customer_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    return await order_service.checkout(customer_id, session)



@order_router.get('/{order_id}',dependencies=[user_role_check])
async def get_order_with_id(order_id:uuid.UUID,session:AsyncSession=Depends(get_session)):
    order=await order_service.get_order(order_id,session)
    if not order :
        raise  OrderNotFound() 
    else:
         return order




@order_router.get('/',dependencies=[user_role_check])
async def get_all_order(session:AsyncSession=Depends(get_session)):
    order=await order_service.get_all_order(session=session)
    return order





@order_router.delete('/{order_id}',dependencies=[user_role_check])
async def delete_order(
    order_id:uuid.UUID,
    session:AsyncSession=Depends(get_session)):
        await order_service.delete_order(order_id,session=session)
        return  {"message": "Order deleted successfully"}


@order_router.patch("/{order_id}", response_model=OrderBase)
async def update_order(
    order_id: uuid.UUID,
    data: OrderUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await order_service.update_order(order_id, data, session)





