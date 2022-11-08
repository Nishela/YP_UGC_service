import random

from config import BOOKMARKS, REVIEWS, VOTES
from utils import get_random_date, MOVIE_IDS, USER_IDS
from faker import Faker

faker = Faker()


def generate_film_review():
    for _ in range(REVIEWS):
        result = dict(
            user_id=random.sample(tuple(USER_IDS), 1)[0],
            movie_id=random.sample(tuple(MOVIE_IDS), 1)[0],
            text=faker.text(),
            timestamp=get_random_date()
        )
        yield result


def generate_film_vote():
    for _ in range(VOTES):
        result = dict(
            user_id=random.sample(tuple(USER_IDS), 1)[0],
            movie_id=random.sample(tuple(MOVIE_IDS), 1)[0],
            rating=random.randint(0, 10),
        )
        yield result


def generate_bookmark():
    for _ in range(BOOKMARKS):
        result = dict(
            user_id=random.sample(tuple(USER_IDS), 1)[0],
            movie_id=random.sample(tuple(MOVIE_IDS), 1)[0],
        )
        yield result
