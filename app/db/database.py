from app.db import session
from sqlalchemy.ext.asyncio import AsyncSession

def get_internal_user_db() -> AsyncSession:
    return session.get_db("user_db")


def get_dev_db() -> AsyncSession:
    return session.get_db("dev_db_postgres")