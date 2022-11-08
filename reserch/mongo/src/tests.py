import random

from faker import Faker
from pymongo import MongoClient, DESCENDING, ReturnDocument

from config import (MONGO_PORT, MONGO_HOST, DB_NAME,
                    BENCHMARK_ITERATIONS)
from utils import (benchmark, get_random_user_id,
                   get_random_movie_id, USER_IDS,
                   MOVIE_IDS, get_random_date)

faker = Faker()

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.get_database(DB_NAME)

BOOKMARKS = db.get_collection("bookmarks")
REVIEWS = db.get_collection("reviews")
VOTES = db.get_collection("votes")


@benchmark(BENCHMARK_ITERATIONS)
def get_avg_rating():
    movie_id = get_random_movie_id(db, "votes")
    like = VOTES.count_documents(
        {"$and": [{"movie_id": movie_id}, {"rating": {"$gt": 4}}]}
    )
    dislike = VOTES.count_documents(
        {"$and": [{"movie_id": movie_id}, {"rating": {"$lt": 5}}]}
    )
    cursor = VOTES.aggregate(
        [
            {"$match": {"movie_id": movie_id}},
            {"$group": {"_id": 0, "total": {"$sum": "$rating"}}},
        ]
    )
    total = list(cursor)[0].get("total")
    avg = total / (like + dislike)
    return round(avg, 2)


@benchmark(BENCHMARK_ITERATIONS)
def get_users_bookmarks():
    user_id = get_random_user_id(db, "bookmarks")
    res = BOOKMARKS.count_documents(
        {"$and": [{"user_id": user_id}, ]}
    )
    return res


@benchmark(BENCHMARK_ITERATIONS)
def get_film_likes():
    movie_id = get_random_movie_id(db, "votes")
    likes = VOTES.count_documents(
        {"$and": [{"movie_id": movie_id}, {"rating": {"$gt": 4}}]}
    )
    return likes


@benchmark(BENCHMARK_ITERATIONS)
def get_film_dislikes():
    movie_id = get_random_movie_id(db, "votes")
    dislikes = VOTES.count_documents(
        {"$and": [{"movie_id": movie_id}, {"rating": {"$lt": 5}}]}
    )

    return dislikes


@benchmark(BENCHMARK_ITERATIONS)
def get_movie_reviews_sort_timestamp():
    movie_id = get_random_movie_id(db, "reviews")
    query = {"movie_id": movie_id}
    res = len(list(REVIEWS.find(query).sort("timestamp", DESCENDING)))
    return res


@benchmark(BENCHMARK_ITERATIONS)
def get_user_likes_movies():
    user_id = get_random_user_id(db, 'votes')
    query = {"user_id": user_id, "rating": {"$gt": 4}}
    likes = VOTES.find(query)
    res = len([rating.get("movie_id") for rating in likes])
    return res


@benchmark(BENCHMARK_ITERATIONS)
def get_user_dislikes_movies():
    user_id = get_random_user_id(db, 'votes')
    query = {"user_id": user_id, "rating": {"$lt": 5}}
    dislikes = VOTES.find(query)
    res = len([rating.get("movie_id") for rating in dislikes])
    return res


@benchmark(BENCHMARK_ITERATIONS)
def add_bookmark():
    user_id = random.sample(tuple(USER_IDS), 1)[0]
    movie_id = random.sample(tuple(MOVIE_IDS), 1)[0]

    bookmark = BOOKMARKS.find_one(
        {"$and": [{"movie_id": movie_id}, {"user_id": user_id}]}
    )
    if bookmark:
        return f"User:{user_id} already have bookmark for movie {movie_id}"

    BOOKMARKS.insert_one({"user_id": user_id, "movie_id": movie_id})
    return f"Added bookmark for movie: {movie_id} to user: {user_id}"


@benchmark(BENCHMARK_ITERATIONS)
def add_review():
    user_id = random.sample(tuple(USER_IDS), 1)[0]
    movie_id = random.sample(tuple(MOVIE_IDS), 1)[0]
    filtered = {"user_id": user_id, "movie_id": movie_id}
    data = {
        "user_id": user_id,
        "text": faker.text(),
        "movie_id": movie_id,
        "timestamp": get_random_date(),
    }

    REVIEWS.find_one_and_replace(
        filtered,
        data,
        projection={"_id": False},
        return_document=ReturnDocument.AFTER,
        upsert=True,
    )
    return f"Added review for movie: {movie_id} from user: {user_id}"


@benchmark(BENCHMARK_ITERATIONS)
def add_vote():
    user_id = random.sample(tuple(USER_IDS), 1)[0]
    movie_id = random.sample(tuple(MOVIE_IDS), 1)[0]
    filtered = {"user_id": user_id, "movie_id": movie_id}
    data = {
        "user_id": user_id,
        "movie_id": movie_id,
        "rating": random.randint(1, 10),
    }

    VOTES.find_one_and_replace(
        filtered,
        data,
        projection={"_id": False},
        return_document=ReturnDocument.AFTER,
        upsert=True,
    )
    return f"Added vote for movie: {movie_id} from user: {user_id}"


@benchmark(BENCHMARK_ITERATIONS)
def remove_bookmark():
    user_id = get_random_user_id(db, "bookmarks")
    cursor = BOOKMARKS.find({"user_id": user_id})
    movie_id = list(cursor)[0].get("movie_id")

    BOOKMARKS.find_one_and_delete(
        {"$and": [{"movie_id": movie_id}, {"user_id": user_id}]},
        projection={"_id": False},
    )

    return f"Successful delete bookmark for movie: {movie_id},  user: {user_id}"


READ_TESTS = (
    get_avg_rating,
    get_users_bookmarks,
    get_film_likes,
    get_film_dislikes,
    get_movie_reviews_sort_timestamp,
    get_user_likes_movies,
    get_user_dislikes_movies,
)
WRITE_TESTS = (
    add_bookmark,
    add_review,
    add_vote,
    remove_bookmark,
)
