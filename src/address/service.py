# src/address/service.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
import uuid
from datetime import datetime

from src.db.model import Address
class AddressService:

    # async def create_address(self, customer_id: uuid.UUID, data, session: AsyncSession):
    #     address = Address(
    #         **data.model_dump(),
    #         cutomer_id=customer_id,
    #         created_at=datetime.utcnow(),
    #         updated_at=datetime.utcnow(),
    #     )
    #     session.add(address)
    #     await session.commit()
    #     await session.refresh(address)
    #     return address

    async def get_addresses(self, customer_id: uuid.UUID, session: AsyncSession):
        result = await session.execute(
            select(Address).where(Address.cutomer_id == customer_id)
        )
        return result.scalars().all()

    async def get_address(self, address_id: uuid.UUID, session: AsyncSession):
        address = await session.get(Address, address_id)
        if not address:
            raise HTTPException(404, "Address not found")
        return address

    async def delete_address(self, address_id: uuid.UUID, session: AsyncSession):
        address = await self.get_address(address_id, session)
        await session.delete(address)
        await session.commit()