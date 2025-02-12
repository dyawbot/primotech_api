from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.model.users import Users
from app.schemas.users import UserSchema
from app.model.helper import StatusHelper
from sqlalchemy.future import select




async def get_users(db:AsyncSession, skip:int=0,limit:int=100):
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
    stmt = select(Users).order_by(Users.id.desc()).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db:AsyncSession, user_id: int):
    try:
        stmt = select(Users).where(Users.userId == user_id)
        result = await db.execute(stmt)


        _user = result.scalar_one_or_none()
        print(_user)

        if _user is None:
            return StatusHelper(code=404, status="Empty", message="User is not registered")
        else:
            return StatusHelper(code=200, status="OK", message="Success getting the user", result=_user)
    except IntegrityError as e:

        return StatusHelper(code= 422, status="Error", message="An error gettitng the user")
    except Exception as e:
        return StatusHelper(code=500, result="Error", message="An unexpected error occured")

    # return _user


async def create_user(db: Session, user: UserSchema):

    _get_last_id =await  get_generated_id(db)

    _get_last_id = _get_last_id.userId[1:]
    _get_incremented_user_id = int(_get_last_id) + 1
    
    _user = Users(userId=f"P{_get_incremented_user_id}", username= user.username)
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


