from pydantic_settings import BaseSettings
import os, typing
from dotenv import load_dotenv
class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    APP_TITLE: str = "Vue FastAPI Admin"
    PROJECT_NAME: str = "Vue FastAPI Admin"
    APP_DESCRIPTION: str = "Description"

    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]

    DEBUG: bool = True
    DB_URL: str  # 确保您有在.env文件中设置这个变量

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")
    SECRET_KEY: str  # openssl rand -hex 32
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    TORTOISE_ORM: dict = {}
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

res = load_dotenv(".env")
print(res)
settings = Settings()
settings.TORTOISE_ORM = {
    "connections": {
        "mysql": settings.DB_URL,
    },
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "mysql",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}