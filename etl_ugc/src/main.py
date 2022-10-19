import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from etl_ugc.src.clickhouse import init_database, save_to_clickhouse

# TODO: вынести в env
CLICKHOUSE_MAIN_HOST = 'clickhouse-node1'
CLICKHOUSE_ALT_HOSTS = ["clickhouse-node2", "clickhouse-node3", "clickhouse-node4"]
KAFKA_TOPICS = 'views'
KAFKA_HOST = '0.0.0.0'
KAFKA_PORT = 9092


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
def insert_to_clickhouse(client: Client, data: list) -> None:
    save_to_clickhouse(client, data)


def etl_process(consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    ...


@backoff.on_exception(backoff.expo, NoBrokersAvailable)
def main() -> None:
    # consumer = KafkaConsumer()
    clickhouse_client = Client(
        host=CLICKHOUSE_MAIN_HOST,
        alt_hosts=CLICKHOUSE_ALT_HOSTS,
    )

    init_database(clickhouse_client)

    # etl_process(consumer, clickhouse_client)


if __name__ == '__main__':
    main()
