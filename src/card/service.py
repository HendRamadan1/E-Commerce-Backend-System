from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
import uuid
from datetime import datetime
from sqlalchemy.orm import selectinload 
from sqlalchemy import delete

from src.db.model import Cart, CartProductLink, Product
from .schema import AddToCart
from src.error import productNotFound,CartNotFound


class CartService:

    # ===============================
    # Get or Create Cart
    # ===============================
    async def get_or_create_cart(
        self, customer_id:uuid.UUID, session: AsyncSession
    ) -> Cart:

        result = await session.execute(
            select(Cart).where(Cart.customer_id == customer_id)
        )
        cart = result.scalar_one_or_none()

        if cart:
            return cart

        cart = Cart(
            customer_id=customer_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(cart)
        await session.commit()
        await session.refresh(cart)
        return cart


    # ===============================
    # Add product to cart
    # ===============================
    async def add_to_cart(
        self,
        customer_id:uuid.UUID,
        data: AddToCart,
        session: AsyncSession,
    ):
        cart = await self.get_or_create_cart(customer_id, session)

        # check product exists
        product = await session.get(Product, data.product_id)
        if not product:
            raise productNotFound()

        # check if already in cart
        result = await session.execute(
            select(CartProductLink).where(
                CartProductLink.cart_id == cart.uid,
                CartProductLink.product_id == data.product_id,
            )
        )
        link = result.scalar_one_or_none()

        if link:
            link.quantity += data.quantity
        else:
            link = CartProductLink(
                cart_id=cart.uid,
                product_id=data.product_id,
                quantity=data.quantity,
            )
            session.add(link)

        cart.updated_at = datetime.utcnow()
        await session.commit()
        return {"message": "Product added to cart"}

    # ===============================
    # Get Cart with items
    # ===============================
    async def get_cart(
        self, customer_id:uuid.UUID, session: AsyncSession
    ) -> Cart:
        result = await session.execute(
            select(Cart)
            .where(Cart.customer_id == customer_id).options(
        selectinload(Cart.items).selectinload(CartProductLink.product)
    )

        )
        cart = result.scalar_one_or_none()

        if not cart:
            raise CartNotFound
        items = []
        for item in cart.items:
            items.append({
                "product_id": item.product_id,
                "product_name": item.product.product_name,
                "price": item.product.mrp,
                "quantity": item.quantity,
            })

        return {
            "uid": cart.uid,
            "customer_id": cart.customer_id,
            "items": items
        }

    async def get_cart_model(
    self, customer_id: uuid.UUID, session: AsyncSession
) -> Cart:
        result = await session.execute(
            select(Cart).where(Cart.customer_id == customer_id)
        )
        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        return cart

    # ===============================
    # Remove product from cart
    # ===============================
    async def remove_from_cart(
        self,
        customer_id: uuid.UUID,
        product_id: uuid.UUID,
        session: AsyncSession,
    ):
        cart = await self.get_cart_model(customer_id, session)

        result = await session.execute(
            select(CartProductLink).where(
                CartProductLink.cart_id == cart.uid,
                CartProductLink.product_id == product_id,
            )
        )
        link = result.scalar_one_or_none()

        if not link:
            raise HTTPException(status_code=404, detail="Product not in cart")

        await session.delete(link)
        await session.commit()

        return {"message": "Product removed from cart"}

    # ===============================
    # Clear cart
    # ===============================
    async def clear_cart(self, customer_id: uuid.UUID, session: AsyncSession):
        cart = await self.get_cart_model(customer_id, session)

        await session.execute(delete(CartProductLink).where(
                CartProductLink.cart_id == cart.uid
            )
        )

        await session.commit()
        return {"message": "Cart cleared"}
    

    async def update_cart_item(
    self,
    customer_id: uuid.UUID,
    product_id: uuid.UUID,
    quantity: int,
    session: AsyncSession,
):
        if quantity < 0:
            raise HTTPException(status_code=400, detail="Quantity cannot be negative")

        cart = await self.get_cart_model(customer_id, session)

        result = await session.execute(
            select(CartProductLink).where(
                CartProductLink.cart_id == cart.uid,
                CartProductLink.product_id == product_id,
            )
        )
        link = result.scalar_one_or_none()

        if not link:
            raise HTTPException(status_code=404, detail="Product not in cart")

        # 🧠 Smart behavior
        if quantity == 0:
            await session.delete(link)
            message = "Product removed from cart"
        else:
            link.quantity = quantity
            message = "Quantity updated"

        cart.updated_at = datetime.utcnow()
        await session.commit()

        return {"message": message}
    
