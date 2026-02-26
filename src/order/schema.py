from pydantic import BaseModel,ConfigDict
from typing import Optional
from src.db.model import Customer,Product
from datetime import datetime
import uuid
from src.db.model import OrderStatus
from  sqlmodel import Field
from src.orderitem.schema import OrderItemsRead

class OrderBase(BaseModel):
    uid:uuid.UUID
    OrderNumber:int
    ShippingDate:datetime
    OrderDate:datetime
    OrderAmount:float
    Cart_id:Optional[uuid.UUID]
    customer_id: Optional[uuid.UUID]
    status: OrderStatus 
    created_at: datetime 
    updated_at: datetime
    items:list[OrderItemsRead] 
    model_config = ConfigDict(from_attributes=True)


class CreateOrder(BaseModel):
    OrderNumber:int
    ShippingDate:datetime
    OrderDate:datetime
    OrderAmount:float
    Cart_id:Optional[uuid.UUID]
    customer_id: Optional[uuid.UUID]
    status: OrderStatus 


class OrderUpdate(BaseModel):
    ShippingDate: datetime = None
    OrderAmount: Optional[float] = None
    status: Optional[OrderStatus] = None




