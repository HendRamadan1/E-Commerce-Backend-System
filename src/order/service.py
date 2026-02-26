from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import  CreateOrder,OrderUpdate
from src.auth.service import CustomerServicee
from src.product.service import ProductService
from src.db.model import Order
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import select,desc
import logging
import random
import uuid 
from src.db.model import Cart
from sqlalchemy.orm import selectinload
from datetime import datetime
from src.error import productNotFound
from src.card.service import CartService
from src.orderitem.schema import CreateOrdeItems
from src.order.schema import OrderBase
from src.orderitem.service import OrderItemService
order_item_services=OrderItemService()
cart_service=CartService()
from src.db.model import (
    Order,
    OrderItem,
    Product,
    OrderStatus
)

class OrderService:
   
    async def checkout(
        self,
        customer_id: uuid.UUID,
        session: AsyncSession,
    ):
        cart=await cart_service.get_cart_model(customer_id,session=session)
        
        if not cart or not cart.items:
            raise HTTPException(400, "Cart is empty")
        
    

        order = Order(
            Cart_id=cart.uid,
            OrderNumber=random.randint(100000, 999999),
            customer_id=customer_id,
            OrderDate=datetime.utcnow(),
            ShippingDate=datetime.utcnow(),
            OrderAmount=0,
            status=OrderStatus.pending,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(order)
        await session.flush() 

        total_amount = 0

        for item in cart.items:
            product = await session.get(Product, item.product_id)
            if not product :
                raise  productNotFound()

            order_item = OrderItem(
                order_id=order.uid,
                product_id=item.product_id,
                quantity=item.quantity,
                MRP=product.mrp,
            )
            
            total_amount += product.mrp * item.quantity
            session.add(order_item)

        # 4️⃣ update total price
        order.OrderAmount = total_amount
        

        # 5️⃣ clear cart
        await cart_service.clear_cart(customer_id,session)

        await session.commit()

        return {
            "message": "Order created successfully",
            "order_id": order.uid,
            "total": total_amount,
        }
        

    async def get_all_order(self, session: AsyncSession):
        result = await session.execute(
            select(Order)
            .options(selectinload(Order.items))
        )
        orders = result.scalars().all()
        return orders
    



    async def get_order(self, order_id: uuid.UUID, session: AsyncSession):
        result = await session.execute(
            select(Order)
            .where(Order.uid == order_id)
            .options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(404, "Order not found")

        return order



    async def delete_order(self, order_id: uuid.UUID, session: AsyncSession):
        order = await self.get_order(order_id, session)
        for item in order.items:
            await session.delete(item)
        await session.delete(order)
        await session.commit()
        return {"message": "Order deleted successfully"}



    async def update_order(
        self,
        order_id: uuid.UUID,
        order_data: OrderUpdate,
        session: AsyncSession
    ) -> Order:
        order = await self.get_order(order_id, session)

        update_data = order_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(order, key, value)

        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order
    
    



    
