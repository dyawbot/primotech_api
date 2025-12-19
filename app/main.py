from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.session import MODEL_REGISTRY,  get_engine
from app.api.v1.router import api_router
from app.api.v2.router import budgetRouter
from app.core.config import settings, UPLOAD_DIR
from contextlib import asynccontextmanager
from loguru import logger

# import ngrok

# import model.users as users


# users.Base.metadata.create_all(bind=engine)
# from app.core.config import settings
# print(" ")
# print(" ")
# print(" ")
# print(" ")
# print(f"Database URL: {settings.db_names}")
# print(f"Secret Key: {settings.secret_key}")
# print(" ")
# print(" ")
# print(" ")
templates = Jinja2Templates(directory="app/templates")

# APPLICATION_PORT = 5000


app = FastAPI(
    title=settings.name,
    version=settings.version,
    # lifespan=lifespan 
)

origin=[    
    "http://localhost:8080",
    "http://192.168.1.4:8080",
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
    for db_name, alias in settings.db_schemas.items():
        metadata = MODEL_REGISTRY[alias]
        engine = get_engine(db_name)
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

@app.get('/',response_class=HTMLResponse, tags=["Root"])
async def Home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# @app.on_event("shutdown")
# async def shutdown_db():
#     await engine.dispose()

app.include_router(api_router)
app.include_router(budgetRouter, prefix="/we-budget", tags=["we-budget"])


