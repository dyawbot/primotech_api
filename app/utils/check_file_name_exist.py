from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.UserModels.users import Images


async def check_image_file_if_exist(db: AsyncSession, filename: str) -> bool:   
    stmt = select(Images).where(Images.image_name == filename)
    result = await db.execute(stmt)
    return len(result.scalars().all()) < 1 #true exist, false not exist