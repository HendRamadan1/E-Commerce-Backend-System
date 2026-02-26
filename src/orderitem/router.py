from fastapi.routing import APIRouter
from src.auth.dependence import RoleCheck
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.db.model import Customer
from src.error import productNotFound
from .service import OrderItemService
from .schema import OrderItemsRead
order_item_service=OrderItemService()
user_role_check=Depends(RoleCheck(['admin','Customer']))
OrderItem_router=APIRouter()



@OrderItem_router.get('/{order_id}',dependencies=[user_role_check])
async def get_order_items(order_id:str,session:AsyncSession=Depends(get_session)):
    OrderItems=await order_item_service.get_order_item(order_id,session)
    return OrderItems




@OrderItem_router.get("/order/{order_id}", response_model=list[OrderItemsRead])
async def list_order_items(order_id: str, session: AsyncSession = Depends(get_session)):
    return await order_item_service.list_order_items(order_id, session)





@OrderItem_router.delete('/{order_id}',dependencies=[user_role_check])
async def delete_review(
    order_id:str,
    session:AsyncSession=Depends(get_session)):
        await order_item_service.delete_order_item(order_item_id=order_id,session=session)
        return None




@OrderItem_router.patch("/{order_item_id}", response_model=OrderItemsRead,dependencies=[user_role_check])
async def update_order_item(order_item_id: str, quantity: int, session: AsyncSession = Depends(get_session)):
    return await order_item_service.update_order_item(order_item_id=order_item_id,quantity=quantity,session=session)
