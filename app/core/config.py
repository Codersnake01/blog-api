from pydantic import AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    DATABASE_URL: AnyUrl
    SECRET_KEY: str

settings = Settings()