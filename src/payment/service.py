from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status,Request
from datetime import datetime
import uuid
import os 
import stripe
from src.address.schema import AddressCreate
from src.db.model import Payment, Order, PaymentStatus, OrderStatus,PaymentMode,Address
from .schema import PaymentCreate

def calculate_payment_amount(order_amount:float,mode:PaymentMode):
    fee=0
    tax=0
    if mode ==PaymentMode.card:
        fee=order_amount*0.025 
    elif mode ==PaymentMode.cash:
        fee=0
    elif mode ==PaymentMode.wallet:
        fee=0

    tax = order_amount * 0.10
    final_amount = order_amount + fee + tax
    return final_amount, fee, tax


class PaymentService:

    async def create_payment(
        self,
        payment_data: PaymentCreate,
        customer_id: uuid.UUID,
        address_data:AddressCreate,
        session: AsyncSession
    ):
        order = await session.get(Order, payment_data.order_id)

        if not order:
            raise HTTPException(404, "Order not found")
        
        address = Address( 
            **address_data.model_dump(),
            cutomer_id=customer_id,
        )
        session.add(address)
        await session.flush() 

        # 2️⃣ check ownership
        if order.customer_id != customer_id:
            raise HTTPException(403, "Not your order")

        # 3️⃣ prevent duplicate payment
        if order.status != OrderStatus.pending:
            raise HTTPException(
                400, "Order already paid or processed"
            )

        # 4️⃣ create payment
        final_amount,fee,tax=calculate_payment_amount(order.OrderAmount,payment_data.mode)
        payment = Payment(
            order_id=order.uid,
            customer_id=customer_id,
            mode=payment_data.mode,
            amount= final_amount,
            fee=fee,
            tax=tax,
            status=PaymentStatus.pending,
            paid_at=datetime.utcnow()
        )
        if payment_data.mode == PaymentMode.card:
            
            payment.transaction_id = f"TXN-{uuid.uuid4().hex[:10]}"
            payment.status = PaymentStatus.success
            order.status = OrderStatus.paid

        elif payment_data.mode == PaymentMode.wallet:
            
            payment.transaction_id = f"WALLET-{uuid.uuid4().hex[:10]}"
            payment.status = PaymentStatus.success
            order.status = OrderStatus.paid

        elif payment_data.mode == PaymentMode.cash:
            # Cash on delivery
            payment.status = PaymentStatus.pending
            order.status = OrderStatus.pending

        else:
            raise HTTPException(400, "Unsupported payment mode")

        session.add(payment)
        order.updated_at = datetime.utcnow()
        session.add(order)
        await session.commit()
        await session.refresh(payment)
        return  payment



    # 🔍 get payment by order
    async def get_payment_by_order(
        self,
        order_id: uuid.UUID,
        session: AsyncSession
    ):
        result = await session.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return result.scalar_one_or_none()
    

    
    # async def handle_success(self, order_id: uuid.UUID, transaction_id: str, session: AsyncSession):
    #     payment = await session.get(Payment,order_id)
    #     order = await session.get(Order, order_id)

    #     if not payment or not order:
    #         raise HTTPException(404, "Payment or Order not found")

    #     payment.status = PaymentStatus.success
    #     payment.transaction_id = transaction_id
    #     payment.paid_at = datetime.utcnow()
    #     order.status = OrderStatus.paid
    #     order.updated_at = datetime.utcnow()

    #     session.add(payment)
    #     session.add(order)
    #     await session.commit()
    #     await session.refresh(payment)
    #     return payment

    # async def handle_failed(self, order_id: uuid.UUID, session: AsyncSession):
    #     payment = await session.get(Payment, order_id)
    #     order = await session.get(Order, order_id)

    #     if payment:
    #         payment.status = PaymentStatus.failed
    #         payment.updated_at = datetime.utcnow()
    #         session.add(payment)

    #     if order:
    #         order.status = OrderStatus.pending
    #         order.updated_at = datetime.utcnow()
    #         session.add(order)

    #     await session.commit()
    #     return {"status": "failed"}
    


    # async def stripe_webhook(self, request: Request, session: AsyncSession):
    #     payload = await request.body()
    #     sig_header = request.headers.get("stripe-signature")
    #     endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    #     try:
    #         event = stripe.Webhook.construct_event(
    #             payload, sig_header, endpoint_secret
    #         )
    #     except Exception as e:
    #         raise HTTPException(400, f"Webhook error: {str(e)}")

    #     if event["type"] == "payment_intent.succeeded":
    #         intent = event["data"]["object"]
    #         order_id = uuid.UUID(intent.metadata["order_id"])
    #         await self.handle_success(order_id, intent.id, session)

    #     elif event["type"] == "payment_intent.payment_failed":
    #         intent = event["data"]["object"]
    #         order_id = uuid.UUID(intent.metadata["order_id"])
    #         await self.handle_failed(order_id, session)

    #     return {"status": "received"}
    