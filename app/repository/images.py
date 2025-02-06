from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.schemas.users import ImagesUsersSchema
from app.model.helper import UserImageHelper, StatusHelper
from app.model.users import Images, Users



async def get_user_id_by_user_id(db = Session, user_id = str):

    # return await db.query(Users).filter(Users.userId == user_id).first()
    stmt = select(Users).where(Users.userId == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() 

async def save_image_data(db: Session, images: UserImageHelper):
    _user = db.query(Users).filter(Users.userId == images.username).first()
    try:
        _images = Images(image_name= images.image_name, image_page=images.image_path, user_id=_user.id)

        db.add(_images)
        await db.commit()
        await db.refresh(_images)

        return StatusHelper(code=200, status="OK", message="User save an image successfully", result= _images)
    except IntegrityError as e:
        print(e)
        return StatusHelper(code=404, status="Error", message=str(e))
    except Exception as e:
        print(e)
        return StatusHelper(code=500, status="Error", message=str(e))
    