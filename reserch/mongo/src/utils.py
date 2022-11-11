import datetime
import functools
import random
import time
import uuid

from config import USERS, MOVIES


def get_id() -> str:
    return str(uuid.uuid4())


USER_IDS = [get_id() for _ in range(USERS)]
MOVIE_IDS = [get_id() for _ in range(MOVIES)]


def get_random_user_id(db, collection, name="user_id"):
    return db.get_collection(collection).aggregate(
        [{"$sample": {"size": 1}}]).next().get(name)


def get_random_movie_id(db, collection, name="movie_id"):
    return db.get_collection(collection).aggregate(
        [{"$sample": {"size": 1}}]).next().get(name)


def get_random_date():
    start = datetime.datetime.strptime("2/12/2011 2:30 PM", "%m/%d/%Y %I:%M %p")
    delta = datetime.datetime.now() - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)

    return start + datetime.timedelta(seconds=random_second)


def benchmark(iterations: int = 1):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            times = []

            for _ in range(iterations):
                start_time = time.perf_counter()
                func(*args, **kwargs)
                end_time = time.perf_counter()
                times.append(end_time - start_time)

            total_time = sum(times)
            avg_time = total_time / iterations

            print(f"Запрос: {func.__name__}")
            print(f"Кол-во итераций теста: {iterations}")
            print(f"Общее время: {total_time} s")
            print(f"Среднее время: {avg_time:.4f} s")
            print('===' * 20)

        return inner

    return wrapper
