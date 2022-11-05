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


class Topics(BaseSettings):
    views = 'views'


class KafkaSettings(BaseSettings):
    host: str = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    topics: str = Field('test')
    group_id: str = Field("group-id")


class Settings(BaseSettings):
    app = AppConfig()
    topics = Topics().dict()
    kafka_settings = KafkaSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
