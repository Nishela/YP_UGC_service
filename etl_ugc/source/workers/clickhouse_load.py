import logging
from typing import List, Dict, Optional

import backoff
from clickhouse_driver import Client

from utils import get_settings
from .click_queries import CREATE_DB, CREATE_TABLE, INSERT_VALUES

__all__ = (
    'ETLClickhouse',
)

settings = get_settings()


class ETLClickhouse:
    def __init__(self, host: str, db_name: str, tables: List[str]):
        self.host = host
        self.db_name = db_name
        self.tables = tables
        self.client = self.get_client()

    @backoff.on_exception(**settings.backoff_settings)
    def get_client(self) -> Client:
        return Client(host=self.host)

    def init_database(self) -> None:
        self.client.execute(CREATE_DB.format(self.db_name))

        for table in self.tables:
            self.client.execute(CREATE_TABLE.format(self.db_name, table))

    def insert(self, data: Dict[str, List[str]]) -> Optional[bool]:
        for event_name, payload in data.items():
            try:
                self.client.execute(INSERT_VALUES.format(self.db_name, event_name),
                                    payload,
                                    types_check=True)
                logging.info('Success insert %d entries in Clickhouse table %s.%s',
                             len(payload), self.db_name, self.db_name)
                return True
            except KeyError as _err:
                logging.exception("Error inserting data to Clickhouse table %s.%s", self.db_name, event_name)

        return None
