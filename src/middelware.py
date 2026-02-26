from fastapi import FastAPI,status
from fastapi.requests import Request
import time
from fastapi.responses import JSONResponse
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
logger=logging.getLogger('uvicorn.access')
logger.disabled=True

def register_middelware(app:FastAPI):
    @app.middleware('http')
    async def create_logging(reqest:Request,call_next):
        start_time=time.time()
        print ("before",start_time)
        response=await call_next(reqest)
        processing_time=time.time()-start_time
        message=f'{reqest.method}-{reqest.url.path},{reqest.client.port}-{reqest.client.host}'
        print("processing_time",processing_time,"messege is :",message)
        return response
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] ,
        allow_methods=["*"],
        allow_headers= ["*"],
        allow_credentials=True,
    
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['localhost','127.0.0.1'],
    )
    


    
