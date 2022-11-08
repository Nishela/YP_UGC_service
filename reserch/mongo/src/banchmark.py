import argparse
import sys

from pymongo import MongoClient

import tests
from config import DB_NAME, MONGO_HOST, MONGO_PORT
from generator import generate_film_review, generate_bookmark, generate_film_vote
from loader import load_film_reviews, load_film_bookmarks, load_film_votes


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true",
                        help="create test benchmark data")
    parser.add_argument("-r", "--read", action="store_true",
                        help="start read benchmarks")
    parser.add_argument("-w", "--write", action="store_true",
                        help="start read benchmarks")
    return parser


if __name__ == "__main__":
    ap = create_argument_parser()
    argv = ap.parse_args(sys.argv[1:])

    if argv.create:
        print("Creating data for benchmarks")
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        db = client.get_database(DB_NAME)

        # generate data
        reviews_generator = generate_film_review()
        bookmarks_generator = generate_bookmark()
        votes_generator = generate_film_vote()
        # upload data
        load_film_reviews(db, reviews_generator)
        load_film_bookmarks(db, bookmarks_generator)
        load_film_votes(db, votes_generator)

    if argv.read:
        print("Running read benchmarks for MongoDB...")
        for test in tests.READ_TESTS:
            test()

    if argv.write:
        print("Running write benchmarks for MongoDB...")
        for test in tests.WRITE_TESTS:
            test()
