from pydantic_settings  import BaseSettings
from pathlib import Path
# from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Default Project")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION",)
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    API_URL : str = os.getenv("API_URL", "http://localhost:8080")
    ADMIN_EMAIL : str = os.getenv("ADMIN_EMAIL", "primotech@gmail.com")
    ADMIN_PASS : str = os.getenv("ADMIN_PASS", "")

    print()
    print()
    print()
    print()
    print(SECRET_KEY)
    print()
    print()
    print()
    print()

    # NGROK_AUTH_TOKEN: str = os.getenv("NGROK_AUTH_TOKEN", "")
    # NGROK_EDGE: str = os.getenv("NGROK_EDGE", "edge:edghts_"  )

    class Config:
        env_file = ".env"   

settings = Settings()
UPLOAD_DIR = Path("assets/images/receipts")
UPLOAD_TRAINING_DIR = Path("assets/training_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
UPLOAD_TRAINING_DIR.mkdir(parents=True, exist_ok=True) 
