import logging

import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import Error

__all__ = ('ETLClickhouse',)


class ETLClickhouse:
    def __init__(self, host: str, db_name: str, tables: list[str]):
        self.host = host
        self.db_name = db_name
        self.tables = tables
        self.client = self.get_client()

    @backoff.on_exception(backoff.expo, Error)
    def get_client(self):
        return Client(host=self.host)

    def init_database(self):
        self.client.execute(
            f"CREATE DATABASE IF NOT EXISTS {self.db_name} ON CLUSTER company_cluster"
        )
        for table in self.tables:
            self.client.execute(
                f"""
                   CREATE TABLE IF NOT EXISTS {self.db_name}.{table} ON CLUSTER company_cluster
                       (
                           event_name String,
                           movie_id String,
                           user_id String,
                           event_data String,
                           timestamp String
                       )
                       Engine=MergeTree()
                   ORDER BY timestamp
                   """
            )

    def insert(self, data: dict):
        for event_name, payload in data.items():
            try:
                self.client.execute(
                    f"INSERT INTO {self.db_name}.{event_name} VALUES",
                    payload,
                    types_check=True,
                )
                logging.info(f'Success insert {len(payload)} entries in Clickhouse table {self.db_name}.{event_name}')
                return True
            except KeyError as _err:
                logging.exception(f"Error inserting data to Clickhouse table {self.db_name}.{event_name}: {_err}")
