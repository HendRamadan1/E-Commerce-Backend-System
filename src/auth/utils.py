from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
import jwt
import uuid
from itsdangerous import URLSafeTimedSerializer
from src.Config import config
from jwt import ExpiredSignatureError, PyJWTError, DecodeError
import logging

# Password hashing
password_context = CryptContext(schemes=['argon2'], deprecated='auto')
EXPIRE_TIME = 3600  # 1 hour default

def generate_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed: str) -> bool: 
    return password_context.verify(password, hashed)

# JWT Tokens
def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        'user': user_data,
        'exp': datetime.utcnow() + (expiry if expiry else timedelta(seconds=EXPIRE_TIME)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }
    token = jwt.encode(payload=payload, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token

def decode_token(token: str) -> dict:
    if not token or token.count(".") != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token format')
    
    try:
        payload = jwt.decode(jwt=token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

# Safe URL token (e.g., email verification)
serializer = URLSafeTimedSerializer(secret_key=config.JWT_SECRET, salt='email-configuration')

def create_safe_url(data: dict) -> str:
    return serializer.dumps(data)

def decode_url_safe_token(token: str, max_age: int = None) -> dict:
    try:
        data = serializer.loads(token, max_age=max_age)
        return data
    except Exception as e:
        logging.error(f"Failed to decode safe URL token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
