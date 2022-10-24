import logging
from logging import config

from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.structs import OffsetAndMetadata, TopicPartition

from utils import get_settings, LOGGING
from workers import ETLClickhouse
from workers import ETLKafkaConsumer
from workers import batcher, transform

settings = get_settings()


def etl(kafka_consumer: KafkaConsumer, ch_driver: ETLClickhouse, batch_size: int = 10):
    ch_driver.init_database()
    logging.info('>>>>  ELT Process was started...  <<<<')

    while True:
        try:
            batches = []
            batch_count = 0
            for message in kafka_consumer:
                batches.append(transform(message))
                batch_count += 1

                if batch_count == batch_size:
                    ch_driver.insert(batcher(batches))
                    batches.clear()
                    batch_count = 0

                    # коммит
                    for topic in settings.kafka_settings.topics:
                        topic_partition = TopicPartition(topic, message.partition)
                        offset = {topic_partition: OffsetAndMetadata(message.offset, None)}
                        kafka_consumer.commit(offset)

        except KafkaError as _err:
            logging.exception(f"Kafka error: {_err}")

        except Error as _err:
            logging.exception(f"ClickHouse error: {_err}")


def main():
    ch_driver = ETLClickhouse(db_name=settings.ch_settings.db,
                              host=settings.ch_settings.host,
                              tables=settings.ch_settings.tables)
    kafka_consumer = ETLKafkaConsumer(host=settings.kafka_settings.host,
                                      topics=settings.kafka_settings.topics,
                                      group_id=settings.kafka_settings.group_id)
    consumer = kafka_consumer.get_consumer()
    ch_driver.init_database()

    etl(consumer, ch_driver, batch_size=settings.app.batch_size)


if __name__ == "__main__":
    config.dictConfig(LOGGING)
    main()
