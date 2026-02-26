from fastapi import APIRouter, Request, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.payment.service import PaymentService
import stripe
from src.auth.dependence import RoleCheck,get_current_user
user_role_check=Depends(RoleCheck(['admin','Customer']))
payment_service=PaymentService()
webhook_router=APIRouter()
@webhook_router.post("/stripe",dependencies=[user_role_check])
async def stripe_webhook(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    return await payment_service.stripe_webhook(request, session)