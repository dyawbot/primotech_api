from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.model.users import Users, Images
from app.schemas.users import UserSchema, RequestUser
from app.model.helper import StatusHelper
from app.core.config import settings
from sqlalchemy.future import select
from app.utils import hash_password as hash
from fastapi import status

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

import re

from app.utils.email_verification import send_verification_email



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def get_users(db:AsyncSession, skip:int=0,limit:int=5):
    # return await db.query(Users).offset(skip).limit(limit).all()


    try:
        stmt = select(Users).offset(skip).limit(limit)
        result = await db.execute(stmt)
        results = result.scalars().all()
        return StatusHelper(code= 200,status= "OK", message="Success Fetch All Users",result= results)

    except InterruptedError as e:
        print(e)

        return StatusHelper(code=422, status= "Entity Error")


    except Exception as e:
        print(f"an exception occured: {e}")
        return StatusHelper(code= 500, status= "Error", message= "An unexpected error occured")
        # pass


#automatically generates userid
async def get_generated_id(db: AsyncSession):
    try:

        stmt = select(Users).order_by(Users.id.desc()).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    except:
        return None





async def create_user(db: Session, user: RequestUser):

    _get_last_id =await  get_generated_id(db)
    if  _get_last_id is not None:
        _get_last_id = _get_last_id.userId[1:]
        _get_incremented_user_id = int(_get_last_id) + 1
    else:
        _get_incremented_user_id = 10001

    _user = Users(userId=f"P{_get_incremented_user_id}", 
                  username= user.username,
                  first_name = user.first_name,
                  last_name = user.last_name,
                  phone_number = user.phone_number,
                  email = user.email,
                  password = hash.hash_password(user.password))
    
   
    try:
        jwt_data = {"sub": _user.userId, "name" : _user.username, "email" : _user.email, "create_at" : datetime.now().timestamp(), "role_type" : "admin"}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data=jwt_data, expires_delta=access_token_expires)
        is_success = send_verification_email(toEmail=_user.email, token=access_token)
        if(is_success):
            print("YES!")
            db.add(_user)
            await db.commit()
            await db.refresh(_user)
            return StatusHelper(code=status.HTTP_201_CREATED, status="OK", message="User created successfully", result=_user)

        else:
            print("FUCK!")
            return StatusHelper(code=400, status="Error", message= "Error sending an email. Please contact developer and ask for this error")


        
        
    except IntegrityError as e:
        await db.rollback()

        error_message = str(e.orig)
        match = re.search(r"Key \(\w+\)=\((.*?)\) already exists", error_message)

        if match:
            error_message = f"{match.group(1)} already exists."
        else:
            error_message = "An unknown error occurred."
        await db.execute(text("SELECT setval(pg_get_serial_sequence('tbl_users', 'id'), max(id)) FROM tbl_users"))
        await db.commit()
    
        return StatusHelper(code=400, status="Error", message= str(error_message))

    except Exception as e:
        
        await db.rollback()
        db.execute(text("SELECT setval(pg_get_serial_sequence('tbl_users', 'id'), max(id)) FROM tbl_users"))
        await db.commit()
        return StatusHelper(code=500, status="Error", message= f"An unexpected error occurred: {str(e)}")
        


    # print(_user.userId)
    # return _user

async def get_all_users_with_images(db: AsyncSession, image_limit: int = 3,  skip:int=5,limit:int=5):

    try:
        stmt = select(Users).order_by(Users.id).offset(skip).limit(limit)
        result = await db.execute(stmt)
        users = result.scalars().all()

        user_images_lists = []

        for user in users:
            image_stmt = select(Images).where(Images.user_id == user.id).order_by(Images.id)
            image_result = await db.execute(image_stmt)
            images = image_result.scalars().all()
            user_images_lists.append({
                "id" :int(user.id),
                "userId": user.userId,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "images": len(images)
            })
            
        print(user_images_lists)
        if not user_images_lists:
            return StatusHelper(code=status.HTTP_404_NOT_FOUND, status= "Error", message= "User not found")
        return StatusHelper(
            code=200,
            status="OK",
            message="User details fetched successfully",
            result=user_images_lists
        )
    except IntegrityError as e:
        return StatusHelper(code= 422, status="Error", message="An error getting the user with images")
    except Exception as e:
        return StatusHelper(code=500, result="Error", message="An unexpected error occured")


async def get_user_by_id(db:AsyncSession, user_id: int, password: str, token: str = None):
    try:
      

        if token:
            user_id = verify_token(token)
            if not isinstance(user_id, str):
                print(type(user_id))
                return user_id

        stmt = select(Users).where(Users.userId == user_id)
        result = await db.execute(stmt) 
        _user = result.scalar_one_or_none()
        
        if _user is None:
            return StatusHelper(code=404, status="Empty", message="User is not registered")
        if  password is not None:
            #the logic for verification of email is in here...
            if(not _user.is_verified):
                return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status="Unverified Email Address", message="Please verify your email address before logging in.")
            if(not hash.verify_password(password, _user.password)):
                return StatusHelper(code=404, status="Empty", message="Wrong password")
            
        # else:
        jwt_data = {"sub": _user.userId, "name" : _user.username, "email" : _user.email, "create_at" : datetime.now().timestamp(), "role_type" : "admin"}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data=jwt_data, expires_delta=access_token_expires)
        return StatusHelper(code=200, status="OK", message="Success getting the user", token=access_token, result=_user)
           
                
    except IntegrityError as e:

        return StatusHelper(code= 422, status="Error", message="An error gettitng the user")
    except Exception as e:
        print(e)
        return StatusHelper(code=500, status="Error", message="An unexpected error occured")
    # return _user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = expire.timestamp()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,  SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= "Invalid token")
        return str(username)
    except JWTError as e:
        print(str(e))
        return StatusHelper(code=status.HTTP_401_UNAUTHORIZED, status= "Error", message= str(e))

        
# def get_user(user_id: str) -> Users: