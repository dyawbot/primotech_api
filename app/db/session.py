from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.config import settings



Base = declarative_base()
BaseWeBudget = declarative_base()


#ENGINES
engine = create_async_engine(settings.DATABASE_URL,echo=True)
webudget_engine = create_async_engine(settings.DB_WEBUDGET_URL, echo=True)


#SESSION MAKERS
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
session_webudget = sessionmaker(autocommit=False, autoflush=False, bind=webudget_engine, class_=AsyncSession)





