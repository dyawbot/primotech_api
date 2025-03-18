from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.model.users import Users, Images
from app.schemas.users import UserSchema, RequestUser
from app.model.helper import StatusHelper
from sqlalchemy.future import select
from app.utils import hash_password as hash
from fastapi import status

import re




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


async def get_user_by_id(db:AsyncSession, user_id: int, password: str):
    try:
        stmt = select(Users).where(Users.userId == user_id)
        result = await db.execute(stmt)
        _user = result.scalar_one_or_none()

        if _user is None:
            return StatusHelper(code=404, status="Empty", message="User is not registered")
      
        if(not hash.verify_password(password, _user.password)):
            return StatusHelper(code=404, status="Empty", message="Wrong password")
            
        
        else:
            return StatusHelper(code=200, status="OK", message="Success getting the user", result=_user)
    except IntegrityError as e:

        return StatusHelper(code= 422, status="Error", message="An error gettitng the user")
    except Exception as e:
        return StatusHelper(code=500, status="Error", message="An unexpected error occured")
    # return _user



async def create_user(db: Session, user: RequestUser):

    _get_last_id =await  get_generated_id(db)
    print("")
    print("")
    print("")
    print(_get_last_id)
    print("")
    print("")
    print("")
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
                  password = hash.hash_password(user.password))
    
   
    try:
        db.add(_user)
        await db.commit()
        await db.refresh(_user)

        return StatusHelper(code=status.HTTP_201_CREATED, status="OK", message="User created successfully", result=_user)
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
                "images": [
                    {"id": img.id, "image_url": img.image_url}
                    for img in images[:3]  
                ]
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

