from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.model.users import Users
from app.schemas.users import UserSchema
from app.model.helper import StatusHelper



def get_users(db:Session, skip:int=0,limit:int=100):
    return db.query(Users).offset(skip).limit(limit).all()

def get_user_by_id(db:Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


async def create_user(db: Session, user: UserSchema):
    _user = Users(userId=user.userId, username= user.username)
    try:
        db.add(_user)
        await db.commit()
        await db.refresh(_user)

        return StatusHelper(code=200, status="OK", message="User created successfully", result=_user)
    except IntegrityError as e:
        await db.rollback()
        error_message = str(e.orig).split("DETAIL:")[1].strip()
        error_message = error_message.replace('"', '').replace('(', '').replace(')', '')
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


