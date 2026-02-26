from __future__ import annotations
from pydantic import BaseModel, Field,ConfigDict
from typing import List
import uuid
from datetime import datetime


class CategoryBase(BaseModel):
    Category_Name: str
    Description: str
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    


class CategoryCreate(BaseModel):
    Category_Name: str
    Description: str

# -------------------
# Schema to update category (input)
# -------------------
class CategoryUpdate(BaseModel):
    Category_Name: str | None = None
    Description: str | None = None

