
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import status


from app.model.helper import StatusHelper


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes()))
    expire = expire.timestamp()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,  settings.secret_key(), algorithm=settings.algorithm())
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key(), algorithms=[settings.algorithm() ])
        username: str = payload.get("sub")
        if username is None:
            return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= "Invalid token")
        return str(username)
    except JWTError as e:
        print(str(e))
        return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= str(e))
