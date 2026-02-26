from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import uuid
from datetime import datetime

class ProductBase(BaseModel):
    product_name: str
    mrp: float
    stock: bool = True
    brand: str


class ProductCreate(BaseModel):
    product_name: str
    mrp: float
    stock: bool = True
    brand: str
    category_id: Optional[uuid.UUID] = None
    # Note: seller_id is NOT her beecause we get it from the JWT Token for security!

class ProductUpdate(BaseModel):
    # All fields are Optional so the seller can update only what they want
    product_name: Optional[str] = None
    mrp: Optional[float] = None
    stock: Optional[bool] = None
    brand: Optional[str] = None
    category_id: Optional[uuid.UUID] = None


class ProductResponse(BaseModel):
    product_name: str
    mrp: float
    stock: bool = True
    brand: str
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    seller_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

