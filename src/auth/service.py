from .schema import UpdateCustomer,CustomerCreateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.db.model import Customer
from .utils import generate_password_hash
class CustomerServicee():

    async def get_user(self,email,session:AsyncSession):
      statement=select(Customer).where(Customer.Email==email)
      result=await session.execute(statement)
      return result.scalar_one_or_none()
      

    async def  user_exist(self,email,session:AsyncSession):
       user= await self.get_user(email,session)
       return True if user is not None else False 
       

    async def update_user(self,user:Customer,user_data:dict,session:AsyncSession):
      
   
          for k,v in user_data.items():
             setattr(user,k,v)
          await session.commit()
          return user
  

              
   

    async def create_user(self,user_data:CustomerCreateModel,session:AsyncSession):
       user_data_dict=user_data.model_dump()
       new_user=Customer(**user_data_dict)
       new_user.hashed_password=generate_password_hash(user_data_dict['hashed_password'])
       new_user.role='Customer'
       session.add(new_user)
       await session.commit()
       return new_user
    
    
    



       