import datetime
import random
import uuid
from typing import Iterator

from reserch.config import get_settings

settings = get_settings()


class DataGenerator:
    FAKE_USER_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]
    FAKE_MOVIE_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]

    def __init__(self, topic):
        self.topic = topic

    def generate_row(self) -> tuple:
        return (
            self.topic,
            random.choice(self.FAKE_USER_IDS),
            random.choice(self.FAKE_MOVIE_IDS),
            random.randint(1, settings.app.max_movie_duration),
            datetime.datetime.now()
        )

    def generate_batch(self, size: int) -> list[tuple]:
        return [self.generate_row() for _ in range(size)]

    def fake_data_generator(self, batch_size: int, quantity: int) -> Iterator:
        return (self.generate_batch(batch_size) for _ in range(quantity))
