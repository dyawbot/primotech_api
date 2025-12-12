from app.db import session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_enum import DBNames

def get_internal_user_db() -> AsyncSession:
    return session.get_db(DBNames.PRIMOUSER.value)


def get_dev_db() -> AsyncSession:
    return session.get_db(DBNames.DEV_DB_POSTGRES.value)


def get_webudget_db() -> AsyncSession:
    return session.get_db(DBNames.WEBUDGET.value)
# import app.db.session as Session

# async def get_db():
#     async with Session.SessionLocal() as db:  
#         try:
#             yield db
#         except Exception as e:
#             await db.rollback()  
#             print(f"(SESSION) An error occured: {e}")
#             raise e
#         finally:
            # await db.close()  



# async def get_db_webudget():
#     async with Session Session.session_webudget() as db:
#         try:
#             yield db
#         except Exception as e:
#             await db.rollback()
#             raise e
#         finally:
#             await db.close()
