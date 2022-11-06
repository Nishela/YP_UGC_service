from typing import List

import backoff
from kafka import KafkaConsumer

from utils import get_settings

__all__ = (
    'ETLKafkaConsumer',
)

settings = get_settings()


class ETLKafkaConsumer:
    def __init__(self, host: List[str], topics: List[str], group_id: str):
        self.host = host
        self.topics = topics
        self.group_id = group_id

    @backoff.on_exception(**settings.backoff_settings)
    def get_consumer(self):
        return KafkaConsumer(
            *self.topics,
            bootstrap_servers=self.host,
            group_id=self.group_id,
            enable_auto_commit=False,
        )
