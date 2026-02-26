from typing import Callable,Any
from fastapi import FastAPI,status
from fastapi.responses import JSONResponse,Response
from  fastapi.requests import Request

class ECommerceBaackend(Exception):
    """this is the base class for project"""
    pass
class InvalidToken(ECommerceBaackend):
      """ User has provided an invalid or expired token"""
      pass


class RefreshToken(ECommerceBaackend):
      """ User has provided an access token when refresh token is needed"""
      pass
    
class AcessToknRequest(ECommerceBaackend):
      """ User has refresh token  when access token is needed"""
      pass


class UserALReadyExists(ECommerceBaackend):
      """ User does not have neccessary premission to  perform an action """
      pass


class InvaliedCrdential(ECommerceBaackend):
      """User has provided wrong email or password during log in."""
      pass

class RvokedToken(ECommerceBaackend):
      """ User has provide a token that has been revoked """
      pass

class Insufficienpermission(ECommerceBaackend):
      """"""
      pass

class UserNotFound(ECommerceBaackend):
      """User not found """
      pass
class AccountNotVerified(ECommerceBaackend):
      """Exception raised when the user account is not verified"""
      pass
class CategoryNotFound(ECommerceBaackend):
      """ Category not found"""
      pass

class productNotFound(ECommerceBaackend):
      """Product is not found"""
      pass

class OrderNotFound(ECommerceBaackend):
      """Order is not found"""
      pass
class CartNotFound(ECommerceBaackend):
      """Cart is not found"""
      pass



def create_exception_handler(status_code:int,intial_detials:Any)->Callable[[Request,Response],JSONResponse]:
      async def acception_handels(request:Request,exc:ECommerceBaackend):
            return JSONResponse(
                  
                  content=intial_detials,
                  status_code=status_code
            )
      
      return acception_handels

def regisiter_error_handel(app:FastAPI):
    app.add_exception_handler(
        UserALReadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            intial_detials={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            intial_detials={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvaliedCrdential,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            intial_detials={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            intial_detials={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RvokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            intial_detials={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AcessToknRequest,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            intial_detials={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            intial_detials={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        Insufficienpermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            intial_detials={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
  
    
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            intial_detials={
                "message": "Account not verified",
                "error_code": "Account not verified",
                "resolution":"Please check your email to verification details"
            },
        ),
    )

    app.add_exception_handler(
        CategoryNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            intial_detials={
              "message": "User not found",
              "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        productNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            intial_detials={
              "message": "prodcut not found",
              "error_code": "product_not_found",
            },
        ),
    )



    app.add_exception_handler(
        OrderNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            intial_detials={
              "message": "order not found",
              "error_code": "order_not_found",
            },
        ),
    )

    app.add_exception_handler(
        CartNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            intial_detials={
              "message": "cart not found",
              "error_code": "cart_not_found",
            },
        ),
    )
   
   
   