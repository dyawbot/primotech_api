from pydantic_settings  import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str = "Primo Tech Api"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:unknownpass@192.168.56.101:5432/postgres"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://postgres:unknownpass@192.168.56.101:5432/postgres"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
  
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
UPLOAD_DIR = Path("assets/images/receipts")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
