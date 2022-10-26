import os
from functools import lru_cache
from typing import Callable

import backoff
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    "get_settings",
)

load_dotenv()
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    batch_size: int = Field(..., env='BATCH_SIZE')


class KafkaSettings(BaseSettings):
    host: str = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    topics: list = Field(..., env='EVENT_TYPES')
    group_id: str = Field(..., env='KAFKA_GROUP_ID')


class ClickHouseSettings(BaseSettings):
    host: str = Field(..., env='CH_HOST')
    db: str = Field(..., env='CH_DB')
    tables: list = Field(..., env='EVENT_TYPES')


class BackoffSettings(BaseSettings):
    wait_gen: Callable = Field(backoff.expo)
    exception: type = Field(Exception)
    max_tries: int = Field(..., env='BACKOFF_MAX_RETRIES')


class Settings(BaseSettings):
    app = AppConfig()
    kafka_settings = KafkaSettings()
    ch_settings = ClickHouseSettings()
    backoff_settings = BackoffSettings().dict()


@lru_cache
def get_settings() -> Settings:
    return Settings()
