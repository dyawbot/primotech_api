import app.db.session as Session

async def get_db():
    async with Session.SessionLocal() as db:  
        try:
            yield db
        except Exception as e:
            await db.rollback()  
            print(f"(SESSION) An error occured: {e}")
            raise e
        finally:
            await db.close()  



async def get_db_webudget():
    async with Session Session.session_webudget() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()