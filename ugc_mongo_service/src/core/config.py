import os
from functools import lru_cache
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from core import LOGGING

__all__ = (
    'get_settings',
)

load_dotenv()
# Применяем настройки логирования
logging_config.fileConfig(LOGGING['log_config'], disable_existing_loggers=True)


class AppConfig(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field('PROJECT_NAME', env='PROJECT_NAME')
    logging = LOGGING


class MongoSettings(BaseSettings):
    host: str = Field(..., env='MONGO_HOST')
    port: int = Field(..., env='MONGO_PORT')


class SentrySetting(BaseSettings):
    pass


class Settings(BaseSettings):
    app = AppConfig()
    mongo = MongoSettings()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
