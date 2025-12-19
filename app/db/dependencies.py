from app.db.db_enum import DBNames
from app.db.session import get_sessionmaker


async def get_db(db_name:str):

    SessionLocal = get_sessionmaker(db_name)
    async with SessionLocal() as session:  
        try:
            yield session
        except Exception as e:
            await session.rollback()  
            print(f"(SESSION) An error occured: {e}")
            raise e
        finally:
            await session.close()  
async def get_internal_user_db():
    # return get_db(DBNames.PRIMOUSER.value)
    async for session in get_db(DBNames.PRIMOUSER.value): 
        yield session


async def get_dev_db():
    # async def get_dev_db() -> AsyncSession:
    async for session in get_db(DBNames.DEV_DB_POSTGRES.value): 
        yield session


async def get_webudget_db():
    print(type(get_db(DBNames.WEBUDGET.value)))
    # return get_db(DBNames.WEBUDGET.value)
    async for session in get_db(DBNames.WEBUDGET.value): 
        yield session