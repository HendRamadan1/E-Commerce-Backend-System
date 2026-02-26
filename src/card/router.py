from fastapi.routing import APIRouter
from src.auth.dependence import RoleCheck,AccessTokenBearer,get_current_user
from fastapi import status , Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.db.model import Customer
from .schema import CreateCart,AddToCart,CartBase,UpdateCart
from src.error import productNotFound
from .service import CartService
import uuid
cart_service=CartService()
user_role_check=Depends(RoleCheck(['admin','Customer']))
cart_router=APIRouter()

@cart_router.post("/add",dependencies=[user_role_check])
async def add_to_cart(
    data: AddToCart,
    current_user: Customer=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await cart_service.add_to_cart(current_user.uid, data, session)


@cart_router.get("/", response_model=CartBase)
async def get_cart(
    current_user: Customer=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await cart_service.get_cart(current_user.uid, session)


@cart_router.delete("/remove/{product_id}")
async def remove_from_cart(
    product_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: Customer=Depends(get_current_user),
):
    return await cart_service.remove_from_cart(current_user.uid, product_id, session)

@cart_router.delete("/clear")
async def clear_the_cart(
     current_user: Customer=Depends(get_current_user),
    session:AsyncSession=Depends(get_session)
):
    return await cart_service.clear_cart(current_user.uid, session)

@cart_router.put("/items/{product_id}")
async def update_cart_item(
    product_id: uuid.UUID,
    data:UpdateCart ,
    session: AsyncSession = Depends(get_session),
    current_user: Customer = Depends(get_current_user),
):
    return await cart_service.update_cart_item(
        customer_id=current_user.uid,
        product_id=product_id,
        quantity=data.quantity,
        session=session,
    )

