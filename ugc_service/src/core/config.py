import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from core import LOGGING

__all__ = (
    'KAFKA_PRODUCER_CONFIG',
    'AVAILABLE_TOPICS',
)

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'UGC')
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AvailableTopics(BaseSettings):
    views = 'views'


class KafkaProducerSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = Field(..., env='KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_TOPIC: str = Field('test')
    KAFKA_CONSUMER_GROUP: str = Field("group-id")


KAFKA_PRODUCER_CONFIG = KafkaProducerSettings()
AVAILABLE_TOPICS = AvailableTopics().dict()
