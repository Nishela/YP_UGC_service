from dataclasses import dataclass
from typing import Any

from kafka_ugc.producer import get_producer


@dataclass
class ModelProducer:
    model: Any

    @staticmethod
    async def async_post_event(instance, topic: str) -> None:
        producer = await get_producer()
        await producer.send_and_wait(
            topic=topic,
            key='+'.join((instance.user_id, instance.data.get('movie_id'))),
            value=instance.data.get('value'),
        )
