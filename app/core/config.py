from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    DATABASE_URL: AnyUrl = AnyUrl("postgresql+asyncpg://user:pass@localhost:5432/db")
    SECRET_KEY: str = "change-me-in-production"
    CLOUDINARY_CLOUD_NAME: str = "qtcyxptv"
    CLOUDINARY_API_KEY: str = "637946757755496"
    CLOUDINARY_API_SECRET: str = "hh2MrNprGvGILJUvC-rxCw1qbio"


settings = Settings()
