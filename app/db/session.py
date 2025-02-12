from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.config import settings



Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_db():
    async with SessionLocal() as db:  
        try:
            yield db
        except Exception as e:
            await db.rollback()  
            print(f"(SESSION) An error occured: {e}")
            raise e
        finally:
            await db.close()  