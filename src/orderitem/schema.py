from pydantic import BaseModel,ConfigDict
from typing import Optional
from src.db.model import Customer,Product
from datetime import datetime
import uuid
from src.db.model import OrderStatus
from  sqlmodel import Field

class OrderItemBase(BaseModel):
    uid:uuid.UUID
    order_id: Optional[uuid.UUID] 
    product_id: Optional[uuid.UUID] 
    quantity: int = Field(ge=1)
    MRP:float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)

class CreateOrdeItems(BaseModel):
    order_id: Optional[uuid.UUID] 
    product_id: Optional[uuid.UUID] 
    quantity: int = Field(ge=1)
    MRP:float


class OrderItemsRead(BaseModel):
    product_id: uuid.UUID
    quantity: int
    MRP: float




