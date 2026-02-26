
from fastapi.routing import APIRouter
from src.auth.dependence import RoleCheck,get_current_user
from fastapi import status , Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.db.model import Customer
from .schema import PaymentBase
import uuid
from src.address.schema import AddressCreate

from src.error import OrderNotFound
from .service import PaymentService,PaymentCreate
payment_service=PaymentService()
user_role_check=Depends(RoleCheck(['admin','Customer']))
payment_router=APIRouter()

@payment_router.post("/", response_model=PaymentBase)
async def pay_order(data: PaymentCreate, address:AddressCreate,session: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)):
    return await payment_service.create_payment(data,customer_id=current_user.uid,address_data=address,session=session)
