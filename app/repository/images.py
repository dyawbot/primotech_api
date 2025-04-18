from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from  fastapi import status, UploadFile
from app.schemas.users import ImagesUsersSchema
from app.model.helper import UserImageHelper, StatusHelper
from app.model.users import Images, Users
from app.utils.check_file_name_exist import check_image_file_if_exist
from app.utils.image_compression import image_compression




async def get_user_id_by_user_id(db = AsyncSession, user_id = str) -> Users:
    stmt = select(Users).where(Users.userId == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() 


async def get_image_by_id_repo(db:AsyncSession, username: str):
    try:
        _user = await get_user_id_by_user_id(db,username)
        if _user is None:
            return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Empty", message="User is not registered")
        else:
           
            stmt = select(Images).where(Images.user_id == _user.id)
            result = await db.execute(stmt)
            _images = result.scalars().all()

            
            if len(_images) < 1:
                return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Empty", message="User does not have any saved images.")
            return StatusHelper(code=status.HTTP_200_OK, status="OK", message="User successfully retrieved the images.", result= _images)
        
    except IntegrityError as e:
        return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Error", message=str(e))
    except Exception as e:
        return StatusHelper(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="Error", message=str(e))


# async def get_all_image_repository(db:AsyncSession, username:str):
#     try:
#         _user = await get_user_id_by_user_id(db,username)
#         if _user is None:
#             return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Empty", message="User is not registered")

#         else:
#             stmt = select(Images).where(Images.user_id == _user.id)
#             result = await db.execute(stmt)
#             _images = result.scalars().all()
#             return StatusHelper(code=status.HTTP_200_OK, status="OK", message="User save an image successfully", result= _images)
        
#     except IntegrityError as e:
#         return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Error", message=str(e))
#     except Exception as e:
#         return StatusHelper(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="Error", message=str(e))
            

async def save_image_data(db: AsyncSession, images: UserImageHelper, image_file: UploadFile):
    try:
        stmt = select(Users).where(Users.userId == images.username)
        _result = await db.execute(stmt)
        _user = _result.scalar_one_or_none()

        if _user is None:
            return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Empty", message="User is not registered")
        else:
            


            if await check_image_file_if_exist(db=db, filename=images.image_name):
                _images = Images(image_name= images.image_name, image_url=images.image_url, user_id=_user.id)
                db.add(_images)
                await db.commit()
                await db.refresh(_images)

                return StatusHelper(code=status.HTTP_200_OK, status="OK", message="User save an image successfully", result= _images)
            else:
                return StatusHelper(code=status.HTTP_422_UNPROCESSABLE_ENTITY,status="existed", message="Image name is already existed")
    except IntegrityError as e:
        print(e)
        return StatusHelper(code=status.HTTP_404_NOT_FOUND, status="Error", message=str(e))
    except Exception as e:
        print(e)
        return StatusHelper(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="Error", message=str(e))
    