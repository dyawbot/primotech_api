from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db.session import engine, Base
from app.api.v1.router import api_router
from app.core.config import settings, UPLOAD_DIR

# import model.users as users


# users.Base.metadata.create_all(bind=engine)
# from app.core.config import settings
print(" ")
print(" ")
print(" ")
print(" ")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Secret Key: {settings.SECRET_KEY}")
print(" ")
print(" ")
print(" ")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

origin=[
    "http://192.168.1.3:8080",
    "http://192.168.1.6:5050",
    "http://192.168.3.96:8080",
    "http://192.168.73.96:8080",
    "http://192.168.168.96:8080"
]



# app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")  




app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get('/', tags=["Root"])
async def Home():
    print("HELLO WOLRD")
    return "Welcome Userssssssss"

@app.on_event("shutdown")
async def shutdown_db():
    await engine.dispose()

app.include_router(api_router)



