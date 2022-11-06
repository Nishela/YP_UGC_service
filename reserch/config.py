from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class AppConfig(BaseSettings):
    unique_ids: int = Field(..., env='BM_UNIQUE_IDS')
    batch_size: int = Field(..., env='BM_BATCH_SIZE')
    batch_count: int = Field(..., env='BM_BATCH_COUNT')
    max_movie_duration: int = Field(..., env='BM_MAX_MOVIE_DURATION')
    benchmark__iterations: int = Field(..., env='BM_ITERATIONS')


class VerticaConfig(BaseSettings):
    host: str = Field('127.0.0.1', env='VERTICA_HOST')
    port: int = Field(5433, env='VERTICA_PORT')
    user: str = Field('dbadmin', env='VERTICA_USER')
    password: str = Field('', env='VERTICA_USER_PASS')
    database: str = Field('docker', env='VERTICA_DB')
    autocommit: bool = Field(True, env='VERTICA_AUTOCOMMIT')


class ClickhouseConfig(BaseSettings):
    host: str = Field('127.0.0.1', env='CH_HOST')
    table: str = 'movies.views'


class Settings(BaseSettings):
    app = AppConfig()
    vertica = VerticaConfig().dict()
    clickhouse = ClickhouseConfig()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
