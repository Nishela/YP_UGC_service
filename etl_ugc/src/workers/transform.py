import logging

from kafka.consumer.fetcher import ConsumerRecord

from models import EventModel

__all__ = ('transform',
           'batcher',)


def transform(data: ConsumerRecord) -> tuple:
    """ Превращаем данные из Кафки в модель EventModel """
    try:
        res = data._asdict()
        event_data = res.get('value').decode('utf-8')
        timestamp = res.get('timestamp')
        event_name = res.get('topic')
        user_id, movie_id = map(str, (res.get('key').decode('utf-8')).split('+'))

        consumer_data = {'event_name': event_name,
                         'movie_id': movie_id,
                         'user_id': user_id,
                         'event_data': event_data,
                         'timestamp': timestamp}

        payload = EventModel(**consumer_data).dict()
        event_name = payload["event_name"]

        return event_name, payload

    except Exception as transform_ex:
        logging.error("Error while transforming data: {0}".format(transform_ex))


def batcher(data: list[tuple]):
    batches = {}
    for i in data:
        event_name, batch_item = i
        if event_name not in batches:
            batches[event_name] = []
        batches[event_name].append(batch_item)

    return batches
