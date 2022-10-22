import logging
from typing import List

import backoff
from clickhouse_driver import Client

from source.utils import BACKOFF_CONFIG
from .click_queries import CREATE_DB, CREATE_TABLE, INSERT_VALUES

__all__ = (
    'ETLClickhouse',
)


class ETLClickhouse:
    def __init__(self, host: str, db_name: str, tables: List[str, ...]):
        self.host = host
        self.db_name = db_name
        self.tables = tables
        self.client = self.get_client()

    @backoff.on_exception(BACKOFF_CONFIG)
    def get_client(self):
        return Client(host=self.host)

    def init_database(self):
        self.client.execute(CREATE_DB, (self.db_name,))

        for table in self.tables:
            self.client.execute(CREATE_TABLE, (self.db_name, table))

    def insert(self, data: dict):
        for event_name, payload in data.items():
            try:
                self.client.execute(
                    INSERT_VALUES,
                    (self.db_name, event_name, payload),
                    types_check=True,
                )
                logging.info(f'Success insert {len(payload)} entries in Clickhouse table {self.db_name}.{event_name}')
                return True
            except KeyError as _err:
                logging.exception(f"Error inserting data to Clickhouse table {self.db_name}.{event_name}: {_err}")
