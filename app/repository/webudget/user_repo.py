from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status



# from app.model.UserModels.users import Users
from app.model.we_budget.users_models import Users
from app.repository.webudget.helpers import create_access_token
from app.schemas.webudget.users.users_shema import UserRegistrationShema
from app.model.helper import StatusHelper
from app.utils import hash_password as hash
from app.core.config import settings
from app.utils.email_verification import send_verification_email
async def user_registration(db:Session, user: UserRegistrationShema):
    try:

        print(user.userId)
        new_user = Users(
            uid = user.userId,
            name = user.name,
            email = user.email,
            password = hash.hash_password(user.password)
        )

        print(new_user)

        jwt_data = {"sub": user.userId, "name" : user.name, "email" : user.email, "create_at" : datetime.now().timestamp(), "role_type" : "user", "type":"webudget"}
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        token = create_access_token(data=jwt_data, expires_delta=access_token_expires)
        is_success = send_verification_email(toEmail=new_user.email, token=token)
        if(is_success):
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return StatusHelper(code=201, status="OK", message="User registered successfully", result=new_user)
        else:
            return StatusHelper(code=400, status="Error", message="Token generation failed")
    except IntegrityError as e:
        # await db.rollback()
        print(str(e))
        return StatusHelper(code=422, status="Error", message="User with given userId or email already exists")
    except Exception as e:
        # await db.rollback()
        print(str(e))
        return StatusHelper(code=500, status="Error", message="An unexpected error occurred during user registration")
    

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
