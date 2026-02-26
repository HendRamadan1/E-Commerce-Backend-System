from pydantic import BaseModel,validator,EmailStr,Field
import uuid 
from datetime import datetime
import re
from typing import List
from src.product.schema import ProductResponse

class CustomerModel(BaseModel):
    uid:uuid.UUID
    FirstName:str
    MiddleName:str
    LastName:str
    Email:str
    username:str
    AGE:int
    is_verified:bool
    hashed_password:str
    DataOfBirth:datetime
    created_at: datetime 
    updated_at: datetime 
    




class UpdateCustomer(BaseModel):
    FirstName:str
    MiddleName:str
    LastName:str
    Email:str
    hashed_password:str
    @validator ('hashed_password')
    def password_complexity(cls,v):
        if len(v) > 8:
            raise ValueError("Password must be at most 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v
            


class CustomerCreateModel(BaseModel):

    FirstName:str=Field(max_length=40)
    MiddleName:str
    LastName:str
    Email:str
    username:str
    AGE:int
    hashed_password:str
    DataOfBirth: datetime 
    @validator ('hashed_password')
    def password_complexity(cls,v):
        if len(v) > 8:
            raise ValueError("Password must be at most 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v
    

class Logging(BaseModel):
   email:str
   hashed_password:str



class CustomerProductModel(BaseModel):
   products:List[ProductResponse]


class passwordResetConfirm(BaseModel) :
     new_password:str
     confirm_new_password:str
     @validator("confirm_new_password")
     def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v
     



class passwordResetRequestModel(BaseModel):
    email:EmailStr


class EmialModel(BaseModel):
   address:List[EmailStr]

