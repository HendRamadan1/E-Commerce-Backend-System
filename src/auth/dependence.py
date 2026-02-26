from fastapi.security import HTTPBearer
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.security.http import HTTPAuthorizationCredentials
from typing import Any, List

from .service import CustomerServicee
from .utils import decode_token
from src.db.main import get_session
from src.db.model import Customer
from src.error import (
    InvalidToken,
    RefreshToken,
    AcessToknRequest,
    Insufficienpermission,
    AccountNotVerified
)
from src.db.redis import token_in_blocklist

customer_service = CustomerServicee()

#
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.valid_token(token):
            raise InvalidToken()

        if await token_in_blocklist(token_data['jti']):
            raise InvalidToken()

        self.vertify_token_data(token_data)
        return token_data

    def valid_token(self, token: str) -> bool:
        return decode_token(token) is not None

    def vertify_token_data(self, token_data: dict):
        raise NotImplementedError("please override this method in child classes")



class AccessTokenBearer(TokenBearer):
    def vertify_token_data(self, token_data: dict):
        if token_data.get("refresh", False):
            raise AcessToknRequest()


class RefreshTokenBearer(TokenBearer):
    def vertify_token_data(self, token_data: dict):
        if not token_data.get("refresh", False):
            raise RefreshToken()



async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
) -> Customer:
    user_email = token_data['user']['email']
    user = await customer_service.get_user(user_email, session)
    if not user:
        raise InvalidToken()
    return user



class RoleCheck:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Customer = Depends(get_current_user)) -> Any:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return True
        raise Insufficienpermission()


