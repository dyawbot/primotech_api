from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.model.UserModels.users import Users, Images
from app.schemas.UserSchemas.users import UserSchema, RequestUser
from app.model.helper import StatusHelper
from app.core.config import settings
from sqlalchemy.future import select
from app.utils import hash_password as hash
from fastapi import status

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

import re

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



async def activate_email(db: AsyncSession, email:str):
    print(email)
    try:
        if email is None:
            return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Error Email", message="Please provide your email to verify or contact the PrimoTech")
        
        stmt = select(Users).where(Users.email == email )
        result = await db.execute(stmt) 
        _user = result.scalar_one_or_none()

        if _user is None:
            return StatusHelper(code=404, status="Empty", message="User with the provided email is not registered.")
        
        
        _user.is_verified = True
        db.add(_user)
        await db.commit()
        return StatusHelper(
            code=status.HTTP_200_OK,
            status="Verified",
            message="Email verification successful."
        )
        
    except Exception as e:
        print("Error during email verification:", e)
        return StatusHelper(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status="Error",
            message="Something went wrong during email verification."
        )
