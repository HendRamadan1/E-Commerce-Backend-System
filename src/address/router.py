# src/address/router.py

from fastapi.routing import APIRouter
from src.auth.dependence import RoleCheck,get_current_user
from fastapi import status , Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.db.model import Customer
from .schema import PaymentBase
import uuid
from.service import AddressService
from.schema import AddressBase
address_router = APIRouter()
user_role_check=Depends(RoleCheck(['admin','Customer']))
service = AddressService()

# @router.post("/", response_model=AddressBase,dependencies=[user_role_check])
# async def create_address(
#     data: AddressCreate,
#     current_user=Depends(get_current_user),
#     session: AsyncSession = Depends(get_session),
# ):
#     return await service.create_address(current_user.uid, data, session)

@address_router.get("/", response_model=list[AddressBase],dependencies=[user_role_check])
async def list_addresses(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await service.get_addresses(current_user.uid, session)



@address_router.delete("/{address_id}",dependencies=[user_role_check])
async def delete_address(
    address_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    await service.delete_address(address_id, session)
    return {"message": "Address deleted"}

