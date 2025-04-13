from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.db.session import engine, Base
from app.api.v1.router import api_router
from app.core.config import settings, UPLOAD_DIR
from contextlib import asynccontextmanager
from loguru import logger
# import ngrok

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

# APPLICATION_PORT = 5000

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("\n\n\n")
#     print("FUCK")
#     print("\n\n\n")
#     logger.info(f"Setting up Ngrok Tunnel {settings.NGROK_AUTH_TOKEN}")
#     ngrok.set_auth_token(settings.NGROK_AUTH_TOKEN)  # ✅ Use environment settings
#     tunnel = ngrok.forward(
#         addr=APPLICATION_PORT,
#         labels=settings.NGROK_EDGE,
#         proto="labeled",
#     )
#     # logger.info(f"Ngrok Tunnel URL: { tunnel.metadata}")
#     yield
#     logger.info("Tearing Down Ngrok Tunnel")
#     ngrok.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    # lifespan=lifespan 
)

origin=[
    "http://localhost:8080",
    "http://192.168.1.5:8080",
    "http://192.168.1.8:8080",
    "https://*.ngrok-free.app"
]



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


# ✅ Run the application
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=APPLICATION_PORT, reload=True)



