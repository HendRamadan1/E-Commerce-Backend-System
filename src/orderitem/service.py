# src/order/order_item_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime
from src.db.model import OrderItem, Product, Order

class OrderItemService:

    async def create_order_item(
        self, order_id: str, product_id: str, quantity: int, MRP: float, session: AsyncSession
    ):
        # check order exists
        order = await session.get(Order, order_id)
        if not order:
            raise HTTPException(404, "Order not found")

        # check product exists
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            MRP=MRP,
            created_at=datetime.utcnow(),
        )
        session.add(order_item)
        await session.commit()
        await session.refresh(order_item)
        return order_item


    async def get_order_item(self, order_item_id: str, session: AsyncSession):
        item = await session.get(OrderItem, order_item_id)
        if not item:
            raise HTTPException(404, "OrderItem not found")
        return item

    async def list_order_items(self, order_id: str, session: AsyncSession):
        result = await session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        items = result.scalars().all()
        return items
    

    async def update_order_item(self, order_item_id: str, quantity: int, session: AsyncSession):
        item = await session.get(OrderItem, order_item_id)
        if not item:
            raise HTTPException(404, "OrderItem not found")

        item.quantity = quantity
        await session.commit()
        await session.refresh(item)
        return item

    async def delete_order_item(self, order_item_id: str, session: AsyncSession):
        item = await session.get(OrderItem, order_item_id)
        if not item:
            raise HTTPException(404, "OrderItem not found")
        await session.delete(item)
        await session.commit()
        return {"message": "OrderItem deleted"}