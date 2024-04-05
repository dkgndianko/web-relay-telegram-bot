from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_PERSISTENCE_PATH: Optional[str]


settings = Settings()