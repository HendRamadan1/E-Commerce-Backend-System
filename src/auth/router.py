from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException 
from src.db.main import get_session
from src.db.model import Customer,Seller
from fastapi import APIRouter,status,Depends
from src.celary_task import send_email
from typing import Optional,List
from src.verify_template import verify_email_template,reset_password_template
from .service import CustomerServicee
from sqlmodel import select
import uuid
from src.seller.schema import SellerRequestModel
from fastapi.responses import HTMLResponse
from .dependence import get_current_user,RoleCheck,AccessTokenBearer,RefreshTokenBearer
from .utils import create_access_token,verify_password,create_safe_url,decode_url_safe_token,generate_password_hash
from fastapi import BackgroundTasks
from .schema import (CustomerCreateModel,
                     Logging,
                     passwordResetConfirm,
                     passwordResetRequestModel,
                     CustomerProductModel,
                     EmialModel)

from src.error import (UserALReadyExists,
                       UserNotFound,
                       InvaliedCrdential)

from src.Config import config
from fastapi.responses import JSONResponse
from datetime import timedelta,datetime
from src.db.redis import add_jti_to_blocklist
customer_service=CustomerServicee()
cutomer_router=APIRouter()
role_checker=RoleCheck(['Customer','seller',"admin"])


@cutomer_router.post('/Signup',status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data:CustomerCreateModel,
    bg_task:BackgroundTasks,
    session:AsyncSession=Depends(get_session)
):
    email=user_data.Email
    user_exist=await customer_service.user_exist(email,session)
    if user_exist:
        raise UserALReadyExists()
    new_user= await customer_service.create_user(user_data,session)
    token =create_safe_url({'email':email})
    link =f'http://{config.DOMAIN}/api/v1/auth/verify/{token}'
    html_message=f"""
                    <h1>Verify your Email address</h1>
                    <p>
                    Please click
                    <a href="{link}">here</a>
                    to verify your email
                    </p>
                    """
    subject="welcom to E-commerce  app"
    send_email.delay([email],subject,html_message)
    return {
          "message":"Account Created! Check email to vertify your account ",
          "user":new_user
    }


@cutomer_router.get("/verify/{token}",responses={
        200: {"description": "Account verified successfully"},
        400: {"description": "Invalid or expired token"},
        404: {"description": "User not found"}
    })

async def verify_user_account(token:str,session:AsyncSession=Depends(get_session)):
   try:
    token_data=decode_url_safe_token(token)
   except:
      token_data=None
   if not token_data :
      raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
   
   user_email=token_data.get('email')
   if user_email: 
        user=await customer_service.get_user(email=user_email,session=session)
        if not user:
          raise UserNotFound()
        await customer_service.update_user(user,{'is_verified':True},session=session)
        return JSONResponse(
        content={'message':"Account Vertified successfully"},
        status_code=status.HTTP_200_OK
        )
   raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='token data is not compelete'
   )


      
@cutomer_router.post('/loging')
async def logging(login_data:Logging ,session:AsyncSession=Depends(get_session)):
   
   email_user=login_data.email
   password=login_data.hashed_password
   user=await customer_service.get_user(email=email_user,session=session)
   if user is not None :
      password_valid=verify_password(password,user.hashed_password)
      if password_valid :
         access_token=create_access_token(user_data={'email':user.Email,'role':user.role,"user_Id":str(user.uid)})
         refresh_token=create_access_token(user_data={'email':user.Email,'role':user.role,"user_Id":str(user.uid)},expiry=timedelta(days=3),refresh=True)
         return JSONResponse(
            content={
            'message':"loging sucessufuly ",
            'access_token':access_token,
            'refresh_token':refresh_token,
            "user":{'email':user.Email,'uid':str(user.uid)}
            }
         )

   raise InvaliedCrdential()







@cutomer_router.post('/password_reset_request')
async def reset_password(email_data:passwordResetRequestModel,sessin:AsyncSession=Depends(get_session)):
   email=email_data.email
   token=create_safe_url(data={'Email':email})
   user=await customer_service.get_user(email,session=sessin)
   link=f'http://{config.DOMAIN}/api/v1/auth/password_reset_confirm/{token}'
   html_message= reset_password_template(link=link,user_name=user.FirstName)
   subject = "🔒 Reset Your Password for Your App"
   send_email.delay([email],subject,html_message)
   return JSONResponse(content={
            "message":"Please check your email for instructuions to reset your password",
            
      },status_code=status.HTTP_200_OK)







   
@cutomer_router.post('/password_reset_confirm/{token}',responses={
        200: {"description": "Password reset successfully"},
        400: {"description": "Passwords do not match or invalid password"},
        404: {"description": "User not found"},
    },
)


async def password_confirm(token:str,data:passwordResetConfirm,session:AsyncSession=Depends(get_session)):
   new_password=data.new_password
   confirm_new_password=data.confirm_new_password
   if new_password != confirm_new_password:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,detail='password not matched'
      )
   token_data=decode_url_safe_token(token)
   if not token_data:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Invalid or expire token')
   user_email=token_data.get('Email')
   if user_email: 
        user=await customer_service.get_user(email=user_email,session=session)
        if not user:
          raise UserNotFound()
        password_hash=generate_password_hash(new_password)
        await customer_service.update_user(user,{'hashed_password':password_hash},session)
        return JSONResponse(
           content={"message": "password reset Seccessfully"},
        status_code=status.HTTP_200_OK,

    )
   return JSONResponse(
      content={'message':'invalid or expired token'},
      status_code=status.HTTP_400_BAD_REQUEST
   )





@cutomer_router.post('/send_email')
async def send_email_to_user(Email:EmialModel,session:AsyncSession=Depends(get_session)):
   email=Email.address
   html='<h1> Welcome in our app<\h1> '
   subject="weclome in E_commerce Backend app"
   send_email.delay( email,subject,html)
   return {"message":"email sent sucessfully"}




@cutomer_router.post('/logout')
async def logout(token_details:dict=Depends(AccessTokenBearer())):
   jti=token_details['jti']
   await  add_jti_to_blocklist(jti)
   return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )



@cutomer_router.get('/refresh_token')
async def get_access_token(token_details:dict=Depends(RefreshTokenBearer())):
   expire_time=token_details['exp']
   if datetime.fromtimestamp(expire_time) > datetime.now():
      access_token=create_access_token(user_data=token_details['user'])
   return JSONResponse(content=
                       {'access_token':access_token}
                       )



@cutomer_router.get('/me',response_model=CustomerProductModel)
async def get_current_user(user=Depends(get_current_user),_:bool=Depends(role_checker)):
   return user 




@cutomer_router.post("/seller-request")
async def request_seller_role(
    data:SellerRequestModel,
    current_user: Customer = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Customer requests to become a seller.
    Sets seller_request_status to "pending".
    """
    
    if current_user.role == "seller":
        raise HTTPException(status_code=400, detail="You are already a seller")
    
    if current_user.seller_request_status == "pending":
        raise HTTPException(status_code=400, detail="Your request is already pending")
    
    current_user.seller_request_status = "pending"
    current_user.requested_store_name = data.store_name
    current_user.requested_phone = data.phone

    
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    
    return JSONResponse(
        content={
            "message": "Seller request submitted successfully",
            "status": current_user.seller_request_status
        },
        status_code=status.HTTP_200_OK
    )



@cutomer_router.patch("/admin/approve-seller/{email}")
async def approve_seller_request(
    email: str,
    approve: bool,
    session: AsyncSession = Depends(get_session)
):
    """
    Admin approves or rejects a pending seller request.
    This forcibly uses the main admin (hendtalba@gmail.com) to approve.
    """
    # استدعاء الـ admin من قاعدة البيانات مباشرة
    result = await session.execute(
        select(Customer).where(Customer.Email == "hendtalba@gmail.com")
    )
    current_admin = result.scalar_one_or_none()
    
    if not current_admin:
        raise HTTPException(status_code=400, detail="Admin account not found")
    
    if current_admin.role != "admin":
        raise HTTPException(status_code=403, detail="Admin account does not have admin role")
    
    # جلب المستخدم الذي قدم طلب seller
    user = await customer_service.get_user(email=email, session=session)
    
    if not user:
        raise UserNotFound()
    
    if user.seller_request_status != "pending":
        raise HTTPException(status_code=400, detail="No pending request for this user")
    
    if approve:
        user.role = "seller"
        user.seller_request_status = "approved"
        seller = Seller(
            customer_id=user.uid,
            phone=user.requested_phone,
            store_name=user.requested_store_name
        )
        session.add(seller)
    else:
        user.seller_request_status = "rejected"
    
    await customer_service.update_user(user, {
        "role": user.role,
        "seller_request_status": user.seller_request_status
    }, session)
    
    return JSONResponse(
        content={
            "message": f"Seller request {'approved' if approve else 'rejected'} by admin {current_admin.Email}",
            "role": user.role,
            "status": user.seller_request_status
        },
        status_code=status.HTTP_200_OK
    )