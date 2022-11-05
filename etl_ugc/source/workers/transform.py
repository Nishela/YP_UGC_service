import logging
from typing import Optional
from collections import defaultdict

from kafka.consumer.fetcher import ConsumerRecord

from etl_models import EventModel

__all__ = (
    'transform',
    'batcher',
)


def transform(data: ConsumerRecord) -> Optional[tuple[str, dict[str, str]]]:
    """ Превращаем данные из Kafka в модель EventModel """
    try:
        transform_data = data._asdict()
        user_id, movie_id = (
            str(item)
            for item in transform_data.get('key').decode('utf-8').split('+')
        )

        consumer_data = {'event_name': transform_data.get('topic'),
                         'movie_id': movie_id,
                         'user_id': user_id,
                         'event_data': transform_data.get('value').decode('utf-8'),
                         'timestamp': transform_data.get('timestamp')}

        payload = EventModel(**consumer_data).dict()

        return payload['event_name'], payload
    except Exception as transform_ex:
        logging.error('Error while transforming data: {0}'.format(transform_ex))
        return None


def batcher(data: list[tuple[str, dict[str, str]]]) -> defaultdict[str, list[dict[str, str]]]:
    batches = defaultdict(list)
    for event_name, event in data:
        batches[event_name].append(event)
    return batches
