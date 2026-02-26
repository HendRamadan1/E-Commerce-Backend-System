from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import ENUM

class SellerProductLink(SQLModel, table=True):
    __tablename__ = "seller_product"
    seller_id: Optional[uuid.UUID] = Field(foreign_key="seller.uid", primary_key=True)
    product_id: Optional[uuid.UUID] = Field(foreign_key="product.uid", primary_key=True)


class PaymentStatus(str, Enum):
    success = "success"
    failed = "failed"
    pending = "pending"


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class PaymentMode(str, Enum):
    cash = "cash"
    card = "card"
    wallet = "wallet"


class Category(SQLModel, table=True):
    __tablename__ = "category"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    Category_Name: str = Field(index=True)
    Description:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
    products: List["Product"] = Relationship(back_populates="category",sa_relationship_kwargs={'lazy':'selectin'})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Product(SQLModel, table=True):
    __tablename__ = "product"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    product_name: str
    mrp: float
    stock: bool=Field(default=True)
    brand: str
    category_id: Optional[uuid.UUID]= Field(foreign_key="category.uid")
    seller_id: uuid.UUID = Field(foreign_key="seller.uid", nullable=False)

    category: Optional[Category] = Relationship(back_populates="products",sa_relationship_kwargs={'lazy':'selectin'})
    sellers: List["Seller"] = Relationship(back_populates="products", link_model=SellerProductLink,sa_relationship_kwargs={'lazy':'selectin'})
    reviews: List["Review"] = Relationship(back_populates="product",sa_relationship_kwargs={'lazy':'selectin'})
    cart_items: List["CartProductLink"] = Relationship(back_populates="product",sa_relationship_kwargs={'lazy':'selectin'})
    order_items: List["OrderItem"] = Relationship(back_populates="product",sa_relationship_kwargs={'lazy':'selectin'})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)



class Seller(SQLModel, table=True):
    __tablename__ = "seller"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False)
    )

    customer_id: uuid.UUID = Field(
        foreign_key="customer.uid",
        nullable=False,
        unique=True
    )

    store_name: str = Field(nullable=True)
    phone: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    rating: float = Field(default=0)
    total_sales: int = Field(default=0)

    #  Relationship
    customer: Optional["Customer"] = Relationship(back_populates="seller")
    products: List["Product"] = Relationship(
        back_populates="sellers",
        link_model=SellerProductLink
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)






class Customer(SQLModel, table=True):
    __tablename__ = "customer"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    FirstName:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
    MiddleName:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
    LastName:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
    Email:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
    username:str
    AGE:int
    is_verified:bool=Field(default=False)
    hashed_password:str=Field(exclude=True)
    seller_request_status: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False),
        default="none"
    )  

    DataOfBirth:datetime
    role:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
    seller: Optional["Seller"] = Relationship(back_populates="customer")
    seller_request_status: str = Field(default="none")
    requested_store_name: Optional[str] = None
    requested_phone: Optional[str] = None


    cart: Optional["Cart"] = Relationship(back_populates="customer",sa_relationship_kwargs={'lazy':'selectin'})
    orders: List["Order"] = Relationship(back_populates="customer",sa_relationship_kwargs={'lazy':'selectin'})
    reviews: List["Review"] = Relationship(back_populates="customer",sa_relationship_kwargs={'lazy':'selectin'})
    payment:List['Payment']=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'})
    address:Optional['Address']=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'})
    created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))




    


class Cart(SQLModel, table=True):
    __tablename__ = "cart"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    customer_id:  Optional[uuid.UUID]= Field(foreign_key="customer.uid")
    customer: Optional[Customer] = Relationship(back_populates="cart",sa_relationship_kwargs={'lazy':'selectin'})
    items: List["CartProductLink"] = Relationship(back_populates="cart",sa_relationship_kwargs={'lazy':'selectin'})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CartProductLink(SQLModel, table=True):
    __tablename__ = "cart_product_link"

    cart_id: Optional[uuid.UUID] = Field(foreign_key="cart.uid", primary_key=True)
    product_id: Optional[uuid.UUID] = Field(foreign_key="product.uid", primary_key=True)
    quantity: int = Field(ge=1)
    cart: Optional[Cart] = Relationship(back_populates="items",sa_relationship_kwargs={'lazy':'selectin'})
    product: Optional[Product] = Relationship(back_populates="cart_items",sa_relationship_kwargs={'lazy':'selectin'})
    


class Order(SQLModel, table=True):
    __tablename__ = "order"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    OrderNumber:int
    ShippingDate:datetime
    OrderDate:datetime
    OrderAmount:float
    Cart_id:Optional[uuid.UUID]=Field(default=None,foreign_key="cart.uid")
    customer_id: Optional[uuid.UUID] = Field(foreign_key="customer.uid")
    status: OrderStatus = Field(sa_column=Column(ENUM(OrderStatus, name="order_status_enum")))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    customer: Optional[Customer] = Relationship(back_populates="orders",sa_relationship_kwargs={'lazy':'selectin'})
    items: List["OrderItem"] = Relationship(back_populates="order",sa_relationship_kwargs={'lazy':'selectin'})
    payment: Optional["Payment"] = Relationship(back_populates="order",sa_relationship_kwargs={'lazy':'selectin'})
    updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_item"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    order_id: Optional[uuid.UUID] = Field(foreign_key="order.uid")
    product_id: Optional[uuid.UUID] = Field(foreign_key="product.uid")
    quantity: int = Field(ge=1)
    MRP:float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    order: Optional[Order] = Relationship(back_populates="items",sa_relationship_kwargs={'lazy':'selectin'})
    product: Optional[Product] = Relationship(back_populates="order_items",sa_relationship_kwargs={'lazy':'selectin'})




class Payment(SQLModel, table=True):
    __tablename__ = "payment"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False)
    )

    order_id: uuid.UUID = Field(foreign_key="order.uid", unique=True)
    customer_id: uuid.UUID = Field(foreign_key="customer.uid")

    mode: PaymentMode = Field(
        sa_column=Column(ENUM(PaymentMode, name="payment_mode_enum"))
    )
    status: PaymentStatus = Field(
        sa_column=Column(ENUM(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.pending)
    )
    amount:float
    transaction_id: Optional[str] = None 
    fee:float
    tax:float
    paid_at: datetime = Field(default_factory=datetime.utcnow)
    order: Optional["Order"] = Relationship(back_populates="payment")
    customer: Optional["Customer"] = Relationship(back_populates="payment")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    


class Review(SQLModel, table=True):
    __tablename__ = "review"

    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    product_id: Optional[uuid.UUID] = Field(foreign_key="product.uid")
    customer_id: Optional[uuid.UUID] = Field(foreign_key="customer.uid")
    rating: int = Field(ge=1, le=5)
    comment: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product: Optional[Product] = Relationship(back_populates="reviews",sa_relationship_kwargs={'lazy':'selectin'})
    customer: Optional[Customer] = Relationship(back_populates="reviews",sa_relationship_kwargs={'lazy':'selectin'})
    



class Address(SQLModel, table=True):
    uid:uuid.UUID=Field(sa_column=Column (pg.UUID(as_uuid=True), 
                                          default=uuid.uuid4,
                                            primary_key=True,
                                              nullable=False))
    
    street: str
    city: str
    state: str
    pincode: str
    cutomer_id: Optional[uuid.UUID]  = Field(foreign_key="customer.uid")
    # Relationships
    customer:Optional['Customer']=Relationship(back_populates='address',sa_relationship_kwargs={'lazy':'selectin'})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
  

# class LoginHistory(SQLModel, table=True):
#     __tablename__ = "login_history"

#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: uuid.UUID = Field(foreign_key="customer.uid")
#     login_time: datetime = Field(default_factory=datetime.utcnow)
#     ip_address: Optional[str] = None
#     device_info: Optional[str] = None
#     is_new_device: bool = Field(default=False)

#     user: Optional[Customer] = Relationship(back_populates="logins")
