from pydantic import BaseModel,ConfigDict
from typing import Optional
from src.db.model import Customer,Product
from datetime import datetime
import uuid
from src.db.model import PaymentMode,PaymentStatus
from  sqlmodel import Field
from src.address.schema import AddressCreate

class PaymentBase(BaseModel):
    uid: uuid.UUID
    order_id: uuid.UUID
    customer_id: uuid.UUID
    amount: float
    mode: PaymentMode
    fee:float
    tax:float
    status: PaymentStatus
    paid_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentCreate(BaseModel):
    order_id: uuid.UUID 
    mode: PaymentMode
 



    