from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
from typing import Optional

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    pincode: str
    cutomer_id:uuid.UUID
    created_at: datetime 
    updated_at: datetime 

    model_config = ConfigDict(from_attributes=True)


class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    pincode: str

