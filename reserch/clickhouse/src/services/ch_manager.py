import time
from typing import Iterator

from clickhouse_driver import Client


__all__ = (
    'ClickhouseManager',
)

from reserch.clickhouse.src.queries import INSERT_QUERY


class ClickhouseManager:
    def __init__(self, host: str):
        self.host = host
        self.client = self.get_client()

    def get_client(self):
        return Client(host=self.host)

    def fill_db(self, data: Iterator):
        total_time = []
        for payload in data:
            start_time = time.perf_counter()
            self.insert(payload)
            res_time = time.perf_counter() - start_time
            total_time.append(res_time)
            print(f"Insert batch: {res_time:.3f}")

        total_time = sum(total_time)
        print(f"Total insert operation time: {total_time:.3f}")

    def insert(self, data: dict):
        self.client.execute(INSERT_QUERY, data,
                            types_check=True)

    def get_data(self, query):
        self.client.execute(query)
