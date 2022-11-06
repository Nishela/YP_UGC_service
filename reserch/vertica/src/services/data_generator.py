import datetime
import random
import uuid
from typing import List, Tuple

from reserch.config import get_settings

settings = get_settings()


class DataGenerator:
    FAKE_USER_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]
    FAKE_MOVIE_IDS = [uuid.uuid4() for _ in range(settings.app.unique_ids)]

    def __init__(self, topic: str):
        self.topic = topic

    def generate_row(self) -> Tuple[str, uuid.UUID, uuid.UUID, int, datetime.datetime]:
        return (
            self.topic,
            random.choice(self.FAKE_USER_IDS),
            random.choice(self.FAKE_MOVIE_IDS),
            random.randint(1, settings.app.max_movie_duration),
            datetime.datetime.now()
        )

    def generate_batch(self, size: int) -> List[Tuple[str, uuid.UUID, uuid.UUID, int, datetime.datetime]]:
        return [self.generate_row() for _ in range(size)]

    def fake_data_generator(self, batch_size: int, quantity: int):
        return (self.generate_batch(batch_size) for _ in range(quantity))
