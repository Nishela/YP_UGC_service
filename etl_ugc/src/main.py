import logging

from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from core import CH_CONFIG, APP_CONFIG
from core import KAFKA_CONSUMER_CONFIG as KAFKA_CONF
from workers import ETLClickhouse
from workers import ETLKafkaConsumer
from workers import batcher, transform


def etl(kafka_consumer: KafkaConsumer, ch_driver: ETLClickhouse, batch_size: int = 10):
    ch_driver.init_database()
    logging.info('>>>>  ELT Process was started...  <<<<')

    while True:
        try:
            batches = []
            for message in kafka_consumer:
                batches.append(transform(message))
                if len(batches) == batch_size:
                    prepared_bathes = batcher(batches)
                    ch_driver.insert(prepared_bathes)
                    batches = []
        except KafkaError as _err:
            logging.exception(f"Kafka error: {_err}")

        except Error as _err:
            logging.exception(f"ClickHouse error: {_err}")


def main():
    ch_driver = ETLClickhouse(db_name=CH_CONFIG.CH_DB,
                              host=CH_CONFIG.CH_HOST,
                              tables=CH_CONFIG.TABLES)
    kafka_consumer = ETLKafkaConsumer(host=KAFKA_CONF.KAFKA_HOST,
                                      topics=KAFKA_CONF.TOPICS,
                                      group_id=KAFKA_CONF.GROUP_ID)
    consumer = kafka_consumer.get_consumer()
    ch_driver.init_database()

    etl(consumer, ch_driver, batch_size=APP_CONFIG.BATCH_SIZE)


if __name__ == "__main__":
    main()
