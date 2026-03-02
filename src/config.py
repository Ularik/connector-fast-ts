from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    URL_TS: str
    URL_VS: str

    model_config = SettingsConfigDict(
        env_file = BASE_DIR  / '.env',
        extra = 'ignore'
    )


settings = Settings()