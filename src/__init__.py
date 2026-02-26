from fastapi import FastAPI,status
from contextlib import asynccontextmanager
from src.db.main import init_db,async_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.product.router import product_router
from src.auth.router import cutomer_router
from src.error import regisiter_error_handel
from fastapi.responses import JSONResponse
from src.catogery.router import category_router
from src.create_admin import create_admin_
from src.db.main import get_session
from src.review.router import review_router
from src.middelware import register_middelware
from src.card.router import cart_router
from src.order.router import order_router
from src.orderitem.router import OrderItem_router
from src.payment.router import payment_router
from src.payment.webhook_router import webhook_router
asynccontextmanager
async def life_span(app:FastAPI):
    print(f'Service is staring...')
    await init_db()
    async with async_session() as session:
     await create_admin_(session)
    yield 
    print(f'Service has been stopped')


version='v1'
app=FastAPI(
   title="ecommerce backend ",
   description='A REST API for a book review web service ',
   version=version  ,
   docs_url=f'/api/{version}/docs' ,#http://localhost:8000/api/v1/docs
   redoc_url=f'/api/{version}/redoc',
   openapi_url=f'/api/{version}/openapi.json',
  
  
   lifespan=life_span
)
regisiter_error_handel(app)
register_middelware(app)
@app.exception_handler(500)
async def internal_servr_error(request,exc):
   return JSONResponse(content={
      "message":"Oops! Somthing went wrong",
      "error_code":"server_error",
   },status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


app.include_router(product_router,prefix=f"/api/{version}/product",tags=['products'])
app.include_router(cutomer_router,prefix=f'/api/{version}/auth',tags=['auth'])
app.include_router(category_router,prefix=f'/api/{version}/category',tags=['category'])
app.include_router(review_router,prefix=f'/api/{version}/reviews',tags=['reviews'])
app.include_router(cart_router,prefix=f'/api/{version}/cart',tags=['cart'])
app.include_router(order_router,prefix=f'/api/{version}/order',tags=['order'])
app.include_router(OrderItem_router,prefix=f'/api/{version}/orderItems',tags=['orderitems'])
app.include_router(payment_router,prefix=f'/api/{version}/payement',tags=['payment'])
app.include_router(webhook_router,prefix=f'/api/{version}/webhook',tags=['webhook_router'])
app.include_router(webhook_router,prefix=f'/api/{version}/webhook',tags=['webhook_router'])