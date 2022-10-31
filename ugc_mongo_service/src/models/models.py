import datetime
from typing import Optional

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Orjson(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmVote(Orjson):
    user_id: str
    movie_id: str
    rating: int


class FilmVoteFilter(Orjson):
    user_id: str
    movie_id: str


class FilmInfo(Orjson):
    movie_id: str
    likes: int
    dislikes: int
    rating: float


class Bookmarks(Orjson):
    user_id: str
    movie_ids: list[str] = []


class Bookmark(Orjson):
    user_id: str
    movie_id: str


class FilmReview(Orjson):
    movie_id: str
    user_id: str
    text: str = Field(max_length=800)
    timestamp: datetime.datetime


class FilmReviewAdd(Orjson):
    movie_id: str
    user_id: str
    text: str


class FilmReviewInfo(FilmReview):
    rating: Optional[int]
