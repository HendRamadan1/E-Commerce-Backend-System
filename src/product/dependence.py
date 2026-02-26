from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from src.db.main import get_session
from src.db.model import Seller, Customer
from fastapi.security import OAuth2PasswordBearer
from src.auth.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Customer:


    payload = decode_token(token)
    user_data = payload.get("user")
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return Customer(uid=UUID(user_data["user_Id"]))

async def get_current_seller_id(
    current_user: Customer = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> UUID:
    
    
    query = select(Seller).where(Seller.customer_id == current_user.uid)
    result = await session.execute(query)
    seller = result.scalar_one_or_none()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not approved as a seller yet"
        )
    return seller.uid

