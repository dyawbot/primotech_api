from typing import Dict, List
from pydantic_settings  import BaseSettings
from pathlib import Path
# from functools import lru_cache
from dotenv import load_dotenv
import os
import yaml

load_dotenv(override=True)


# CONFIG_PATH = Path("app_settings.yaml")

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "app_secrets.yaml"


class Config:
    def __init__(self, config_file: Path  = CONFIG_PATH):
        with open(config_file, 'r') as file:
            self._config = yaml.safe_load(file)

    @property
    def name(self) -> str:
        return self._config.get("name", "Default Project")
                                
    @property
    def version(self) -> str:
        return self._config.get("version", "0.1.0")
    
    @property
    def db_global(self) -> Dict[str, str]:
        return self._config["databases"]["global"]
    @property
    def db_names(self) -> List[str]:
        return self._config["databases"]["name"]
    @property
    def db_schemas(self) -> Dict[str, str]:
        """
        Returns dict of {db_name: alias}
        Example: {"user_db": "user", "product_db": "product"}
        """
        return self._config["databases"]["schemas"]
    
    @property
    def email(self) -> Dict[str, str]:
        return self._config.get("email", {})    

    @property
    def secret_key(self) -> str:
        return self._config.get("secret_key", "")         
    @property
    def algorithm(self) -> str:
        return self._config.get("algorithm", "HS256")
    @property
    def access_token_expire_minutes(self) -> int:
        return self._config.get("access_token_expire_minutes", 30)
    
    def build_db_url(self, db_name: str,async_driver: bool = True) -> str:
        g = self.db_global
        driver = "postgresql+asyncpg" if async_driver else "postgresql+psycopg2"
        return f"{driver}://{g['user']}:{g['password']}@{g['host']}:{g['port']}/{db_name}"
    

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Default Project")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION",)

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    API_URL : str = os.getenv("API_URL", "http://localhost:8080")
    ADMIN_EMAIL : str = os.getenv("ADMIN_EMAIL", "primovative@gmail.com")
    ADMIN_PASS : str = os.getenv("ADMIN_PASS", "")


    #DATABASE
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    USER_URL_DATABASE: str = os.getenv("USER_URL_DATABASE")
    #DATABASE SYNC
    USER_URL_DATABASE_SYNC: str = os.getenv("USER_URL_DATABASE_SYNC")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC")

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





settings = Config()
UPLOAD_DIR = Path("assets/images/receipts")
UPLOAD_TRAINING_DIR = Path("assets/training_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
UPLOAD_TRAINING_DIR.mkdir(parents=True, exist_ok=True) 
