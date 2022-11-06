import time
from typing import Dict

from reserch.clickhouse.src.queries import SELECT_QUERIES
from reserch.clickhouse.src.services.ch_manager import ClickhouseManager
from reserch.clickhouse.src.services.data_generator import DataGenerator
from reserch.config import get_settings

settings = get_settings()
ch = ClickhouseManager(settings.clickhouse.host)


def benchmark_queries(query: str, iteration: int = 1, verbose: bool = False) -> None:
    """ Замер времени на различные запросы """
    operation_time = []
    for i in range(1, iteration + 1):
        start_time = time.perf_counter()
        ch.get_data(query)
        cur_time = time.perf_counter() - start_time
        if verbose:
            print(f"attempt {i}/{iteration}: {cur_time}")
        operation_time.append(cur_time)

    total_time = sum(operation_time)
    avg_time = total_time / iteration
    print(f"\ntotal time: {total_time:.3f}")
    print(f"average time: {avg_time:.3f}")


def benchmark_insert() -> None:
    """
    Поток вставки данныx. Кол-во записей = batch_size * batch_count
    """
    # preparing
    fake_gen = DataGenerator('views')
    fake_data = fake_gen.fake_data_generator(batch_size=settings.app.batch_size, quantity=settings.app.batch_count)

    # inserting
    ch.fill_db(fake_data)


def run(requests: Dict[str, str], iteration: int, verbose=False) -> None:
    print("Running benchmarks for CH:")
    for name, query in requests.items():
        print(f"Start: {name}")
        benchmark_queries(query, iteration, verbose)
        print("===" * 10)


def benchmark_select() -> None:
    run(SELECT_QUERIES, 10)
