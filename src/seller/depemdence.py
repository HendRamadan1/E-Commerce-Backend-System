from fastapi import Depends, HTTPException, status
from src.auth.dependence import get_current_user,get_session
import uuid
from src.db.model import Customer
from sqlalchemy.ext.asyncio import AsyncSession
from src.product.service import ProductService
from src.product.dependence import get_current_seller_id
product_service=ProductService()

async def require_seller(current_user: Customer = Depends(get_current_user)) -> Customer:
    """
    Ensure the current user has seller role.
    """

    if current_user.role.lower() != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seller privileges required",
        )

    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account must be verified to perform this action",
        )

    return current_user

async def check_product_owner(
    product_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    seller_id: uuid.UUID = Depends(get_current_seller_id), # We use your bridge here
):
    product = await product_service.get_product(product_id, session)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Business Logic: Is the logged-in seller the one who created this?
    if product.seller_id != seller_id:
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to modify this product."
        )

    return product