from pydantic import BaseModel,ConfigDict
from typing import Optional

from datetime import datetime
import uuid
from  sqlmodel import Field
from typing import List


class CartProductLink(BaseModel):

    product_id: uuid.UUID
    quantity: int 
    product_name:str
    price: float
    model_config = ConfigDict(from_attributes=True)

class CartBase(BaseModel):
    

    uid:uuid.UUID
    customer_id: uuid.UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(from_attributes=True)
    items: List["CartProductLink"] =[]

    
class CreateCart(BaseModel):
     
     customer_id: uuid.UUID

class AddToCart(BaseModel):
    product_id: uuid.UUID
    quantity: int

class UpdateCart(BaseModel):
    quantity:int

