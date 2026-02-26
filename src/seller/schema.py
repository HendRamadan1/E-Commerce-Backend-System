from pydantic import BaseModel,validator,EmailStr,Field
import uuid 

from typing import List
from src.product.schema import ProductBase


class SellerRequestModel(BaseModel):
    store_name: str
    phone: str


