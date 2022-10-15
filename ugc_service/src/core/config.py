import os
from logging import config as logging_config
from typing import Callable

import backoff as backoff
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from src.core import LOGGING

__all__ = (
    'BACKOFF_CONFIG',
)

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'UGC')
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BackoffSettings(BaseSettings):
    wait_gen: Callable = Field(backoff.expo)
    exception: type = Field(Exception)
    max_tries: int = Field(..., env='BACKOFF_MAX_RETRIES')


BACKOFF_CONFIG = BackoffSettings().dict()
