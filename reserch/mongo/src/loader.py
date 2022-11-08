import time

from config import BOOKMARKS, VOTES, REVIEWS


def load_film_reviews(db, data):
    print("Starting upload film reviews")
    start_time = time.perf_counter()
    collection = db.get_collection("reviews")
    collection.insert_many(data, ordered=False)
    perf_time = time.perf_counter() - start_time
    print(f"Uploaded film reviews is done! Total time to load {REVIEWS} reviews: {perf_time:.2f}")


def load_film_votes(db, data):
    print("Starting upload film votes")
    start_time = time.perf_counter()
    collection = db.get_collection("votes")
    collection.insert_many(data, ordered=False)
    perf_time = time.perf_counter() - start_time
    print(f"Uploaded film votes is done! Total time to load {VOTES} votes: {perf_time:.2f}")


def load_film_bookmarks(db, data):
    print("Starting upload film bookmarks")
    start_time = time.perf_counter()
    collection = db.get_collection("bookmarks")
    collection.insert_many(data, ordered=False)
    perf_time = time.perf_counter() - start_time
    print(f"Uploaded film bookmarks is done! Total time to load {BOOKMARKS} bookmarks: {perf_time:.2f}")
