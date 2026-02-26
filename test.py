# from fastapi import status
# from typing import Optional,List
# from sqlmodel import SQLModel ,Column,Field,Relationship
# import  sqlalchemy.dialects.postgresql as pg
# import uuid
# from datetime import datetime
# import enum

# class OrderStatus(str, enum.Enum):
#     PENDING = "pending"
#     SHIPPED = "shipped"
#     DELIVERED = "delivered"
#     CANCELLED = "cancelled"

# class PaymentMode(str, enum.Enum):
#     CREDIT_CARD = "credit_card"
#     PAYPAL = "paypal"
#     CASH = "cash"

# class CartProductLink(SQLModel, table=True):
#    product_id:uuid.UUID=Field(default=None,foreign_key='Product.uid',primary_key=True)
#    cart_id:uuid.UUID=Field(default=None,foreign_key='Cart.Cart_id',primary_key=True)



# class sellerProductLink(SQLModel, table=True):
#    product_id:uuid.UUID=Field(default=None,foreign_key='Product.uid',primary_key=True)
#    seller_id:uuid.UUID=Field(default=None,foreign_key='Saller.uid',primary_key=True)


# class Product(SQLModel,table=True):
#     __tablename__='product'
#     uid : uuid.UUID=Field(sa_column=Column
#                                  (pg.UUID(as_uuid=True),
#                                    default=uuid.uuid4,
#                                    primary_key=True,
#                                    nullable=False))
 
#     product_name:str=Field(sa_column=Column(pg.VARCHAR,nullable=False))
#     seller_id:Optional[uuid.UUID]=Field(default=None,foreign_key='Saller.uid')
#     MRP:float
#     stock:bool 
#     Category_id:Optional[uuid.UUID]=Field(default=None,foreign_key="Category.uid")
#     Category:Optional["Category"]=Relationship(back_populates='product',sa_relationship_kwargs={'lazy':'selectin'}) 
#     Brand:str =Field(sa_column=Column(pg.VARCHAR,nullable=False))
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     cart:List['Cart']=Relationship(link_model=CartProductLink,back_populates='product',sa_relationship_kwargs={'lazy':'selectin'})
#     saller:List['Saller']=Relationship(link_model=sellerProductLink,back_populates='product',sa_relationship_kwargs={'lazy':'selectin'})
#     order_items:List["OrderItem"]=Relationship(back_populates='product',sa_relationship_kwargs={'lazy':'selectin'})
#     reviews: List["Review"] = Relationship(back_populates="product",sa_relationship_kwargs={'lazy':'selectin'})

#     def __repr__(self):
#         return f'product{self.product_name}>'




# class Saller(SQLModel,table=True):
#     __tablename__='Saller'
#     uid:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True),
#             default=uuid.uuid4,
#             primary_key=True,
#             nullable=False)
            
#             )  
    
#     Name:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     Phone:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     Total_Saler:float 
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     product:List['Saller']=Relationship(link_model=sellerProductLink,back_populates='saller',sa_relationship_kwargs={'lazy':'selectin'})

#     def __repr__(self):
#         return f'Saller{self.Name}>'





# class Customer(SQLModel,table=True):
#     __tablename__='Customer'
#     uid:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True),
#             default=uuid.uuid4,
#             primary_key=True,
#             nullable=False)
            
#             )
    
#     FirstName:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     MiddleName:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     LastName:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     Email:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     username:str
#     AGE:int
#     is_verified:bool=Field(default=False)
#     hassed_password:str=Field(exclude=True)
#     DataOfBirth:datetime
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     reviews: List["Review"]=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'}) # one to many 
#     Ordes: List["order"]=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'}) # one to many
#     Payment: List["payment"]=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'}) # one to many  
#     cart:Optional["Cart"]=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'}) 
#     address:Optional["address"]=Relationship(back_populates='customer',sa_relationship_kwargs={'lazy':'selectin'}) 
#     def __repr__(self):
#         return f'Customer{self.FirstName}>'
    




    
# class Category(SQLModel,table=True):
#     __tablename__='Category'
#     uid:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True),
#             default=uuid.uuid4,
#             primary_key=True,
#             nullable=False)
            
#             )
    
#     Category_Name: str = Field(index=True)
#     Description:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     product:List["Product"]=Relationship(back_populates='Category',sa_relationship_kwargs={'lazy':'selectin'}) 

#     def __repr__(self):
#         return f'Category{self.Category_Name}>'




# class Cart(SQLModel,table=True):
#     __tablename__='Cart'
#     Cart_id:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True),
#             default=uuid.uuid4,
#             primary_key=True,
#             nullable=False)
            
#             )
    
#     Customer_id:Optional[uuid.UUID]=Field(default=None,foreign_key='Customer.uid')
#     product_id:Optional[uuid.UUID]=Field(default=NotImplemented,foreign_key="Product.uid")
#     GrandTotal:float
#     itemsTotal:int
#     customer:Optional["Customer"]=Relationship(back_populates='cart',sa_relationship_kwargs={'lazy':'selectin'})
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     product:List['Product']=Relationship(link_model=CartProductLink,back_populates='cart',sa_relationship_kwargs={'lazy':'selectin'})

#     def __repr__(self):
#         return f'Cart{self.itemsTotal}>'
    




# class Review(SQLModel,table=True):
#     __tablename__='Review'
#     Review_id:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True),
#             default=uuid.uuid4,
#             primary_key=True,
#             nullable=False)
            
#             )
    
#     Description:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     rating:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     product_productid:int
#     Customer_id:int 
#     Customer:Optional['Customer']=Relationship(link_model=CartProductLink,back_populates='reviews',sa_relationship_kwargs={'lazy':'selectin'})
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))

#     def __repr__(self):
#         return f'Review{self.Description}>'
    



# class order(SQLModel,table=True):
#     __tablename__='Order'
#     uid:uuid.UUID=Field(sa_column=Column(pg.UUID(as_uuid=True),
#             default=uuid.uuid4,
#             primary_key=True,
#             nullable=False)
            
#             )
    
#     OrderNumber:int
#     ShippingDate:datetime
#     OrderDate:datetime
#     OrderAmount:float
#     Cart_id:Optional[uuid.UUID]=Field(default=None,foreign_key="Cart.uid")
#     Customer_id:Optional[uuid.UUID]=Field(default=None,foreign_key="Customer.uid")
#     orderStatus: OrderStatus = Field(sa_column=Column(enum.Enum(OrderStatus)))
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))   
#     items: List["OrderItem"] = Relationship(back_populates="order",sa_relationship_kwargs={'lazy':'selectin'})
#     payment: Optional["payment"] = Relationship(back_populates="order",sa_relationship_kwargs={'lazy':'selectin'}) 
#     customer: List["Customer"]=Relationship(back_populates='Ordes',sa_relationship_kwargs={'lazy':'selectin'})


#     def __repr__(self):
#         return f'Order{self.OrderNumber}>'
    



# class OrderItem(SQLModel,table=True):
#     __tablename__='OrderItems'
#     uid:uuid.UUID=Field(sa_column=Column
#                                  (pg.UUID(as_uuid=True),
#                                    default=uuid.uuid4,
#                                    primary_key=True,
#                                    nullable=False))
    
#     Product_id:Optional[uuid.UUID]=Field(default=None,foreign_key="Product.uid")
#     MRP:float
#     Quantity:int  
#     order: Optional["order"] = Relationship(back_populates="items",sa_relationship_kwargs={'lazy':'selectin'}) 
#     product: Optional["Product"] = Relationship(back_populates="order_items",sa_relationship_kwargs={'lazy':'selectin'}) 
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))

#     def __repr__(self):
#         return f'OrderItems{self.order}>'

    

# class payment(SQLModel,table=True):
#     __tablename__='OrderItems'
#     uid:uuid.UUID=Field(sa_column=Column
#                                  (pg.UUID(as_uuid=True),
#                                    default=uuid.uuid4,
#                                    primary_key=True,
#                                    nullable=False))
    
#     order_id:Optional[uuid.UUID]=Field(default=None,foreign_key="order.uid")
#     paymentMode:PaymentMode = Field(sa_column=Column(enum.Enum(PaymentMode)))
#     Customer_id:Optional[uuid.UUID]=Field(default=None,foreign_key='Cutomer.uid')
#     Date_of_payment:datetime = Field(default_factory=datetime.utcnow)
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     order: Optional["order"] = Relationship(back_populates="payment",sa_relationship_kwargs={'lazy':'selectin'})
#     customer: Optional["Customer"] = Relationship(back_populates="Payment",sa_relationship_kwargs={'lazy':'selectin'})

#     def __repr__(self):
#         return f'OrderItems{self.paymentMode}>'

    

# class address(SQLModel,table=True):
#     __tablename__="Address"
#     AddressID:uuid.UUID=Field(sa_column=Column
#                                  (pg.UUID(as_uuid=True),
#                                    default=uuid.uuid4,
#                                    primary_key=True,
#                                    nullable=False))
    
#     streetName:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     Apartmet_NO:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     City:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     state:str=Field(sa_column=Column(pg.VARCHAR),nullable=False)
#     pincode:int
#     customer_id:int
#     created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     updated_at: datetime =Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
#     customer: Optional["Customer"] = Relationship(back_populates="address",sa_relationship_kwargs={'lazy':'selectin'})

#     def __repr__(self):
#         return f'OrderItems{self.Product_id}>'

    



