import datetime
import random
import uuid
from typing import Iterator, Union, List, Dict

from reserch.config import get_settings

settings = get_settings()

__all__ = (
    'DataGenerator',
)


class DataGenerator:
    FAKE_USER_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]
    FAKE_MOVIE_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]
    FAKE_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]

    def __init__(self, topic):
        self.topic = topic

    def generate_row(self) -> Dict[str, Union[str, uuid.UUID, datetime.datetime, int]]:
        return {
            'id': random.choice(self.FAKE_IDS),
            'event_name': self.topic,
            'user_id': random.choice(self.FAKE_USER_IDS),
            'movie_id': random.choice(self.FAKE_MOVIE_IDS),
            'event_data': random.randint(1, settings.app.max_movie_duration),
            'timestamp': datetime.datetime.now()
        }

    def generate_batch(self, size: int) -> List[Dict[str, Union[str, uuid.UUID, datetime.datetime, int]]]:
        return [self.generate_row() for _ in range(size)]

    def fake_data_generator(self, batch_size: int, quantity: int) -> Iterator:
        return (self.generate_batch(batch_size) for _ in range(quantity))
