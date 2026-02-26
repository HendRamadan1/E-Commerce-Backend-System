from pydantic import BaseModel
from typing import Optional
from src.db.model import Customer,Product
from datetime import datetime
import uuid
from  sqlmodel import Field

class Review(BaseModel):

    uid: uuid.UUID 
    rating: int=Field(lt=5)
    comment: str 
    product_id: Optional[uuid.UUID] 
    customer_id: Optional[uuid.UUID] 
    created_at: datetime 
    update_at: datetime 


class Create_Review(BaseModel):
    rating: int=Field(lt=5)
    comment: str 