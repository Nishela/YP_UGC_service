import datetime
import logging
from logging import config as logging_config

from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from kafka.structs import OffsetAndMetadata, TopicPartition

from utils import get_settings, LOGGING
from workers import ETLClickhouse
from workers import ETLKafkaConsumer
from workers import batcher, transform

settings = get_settings()
cycle_time = datetime.timedelta(seconds=10)


def etl(kafka_consumer: KafkaConsumer, ch_driver: ETLClickhouse, batch_size: int = 1000):
    ch_driver.init_database()
    logging.info('>>>>  ELT Process was started...  <<<<')
    timer = datetime.datetime.now()

    while True:
        try:
            batches = []
            batch_count = 0
            for message in kafka_consumer:
                time_delta = datetime.datetime.now() - timer
                batches.append(transform(message))
                batch_count += 1

                if batch_count == batch_size or cycle_time < time_delta:
                    ch_driver.insert(batcher(batches))

                    # коммит
                    for topic in settings.kafka_settings.topics:
                        topic_partition = TopicPartition(topic, message.partition)
                        offset = {topic_partition: OffsetAndMetadata(message.offset, None)}
                        kafka_consumer.commit(offset)

                    batches.clear()
                    batch_count = 0
                    timer = datetime.datetime.now()
                    logging.info('>>>>  TIMER refreshed <<<<')

        except KafkaError as _err:
            logging.exception("Kafka error")

        except Error as _err:
            logging.exception("ClickHouse error")


if __name__ == "__main__":
    logging_config.fileConfig(LOGGING['log_config'], disable_existing_loggers=True)
    logging.info('>>>>  CHECK <<<<')
    ch_driver = ETLClickhouse(db_name=settings.ch_settings.db,
                              host=settings.ch_settings.host,
                              tables=settings.ch_settings.tables)
    kafka_consumer = ETLKafkaConsumer(host=settings.kafka_settings.host,
                                      topics=settings.kafka_settings.topics,
                                      group_id=settings.kafka_settings.group_id)
    consumer = kafka_consumer.get_consumer()
    ch_driver.init_database()

    etl(consumer, ch_driver, batch_size=settings.app.batch_size)
