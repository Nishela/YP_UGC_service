import time
from contextlib import contextmanager

import vertica_python
from vertica_python.vertica.connection import Connection

from reserch.config import get_settings
from reserch.vertica.src.queries import DROP_TABLE, CREATE_TABLE, INSERT_VALUES

settings = get_settings()


class VerticaManager:
    @contextmanager
    def _cursor(self) -> Connection:
        connection = vertica_python.connect(**settings.vertica)
        try:
            cursor = connection.cursor()
            yield cursor
        finally:
            connection.close()

    def create_table(self):
        with self._cursor() as cursor:
            cursor.execute(DROP_TABLE)
            cursor.execute(CREATE_TABLE)

    def fill_db(self, data) -> None:
        total_time = []
        with self._cursor() as cursor:
            for payload in data:
                start_time = time.perf_counter()
                cursor.executemany(INSERT_VALUES, payload)
                res_time = time.perf_counter() - start_time
                total_time.append(res_time)
                print(f"Insert batch time: {res_time:.3f}")

        sum_time = sum(total_time)
        print(f"Total insert operation time: {sum_time:.3f}")

    def get_data(self, query):
        with self._cursor() as cursor:
            cursor.execute(query)
