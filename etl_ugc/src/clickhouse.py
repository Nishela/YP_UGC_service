from typing import List

from clickhouse_driver import Client
from etl_ugc.src.models.event_model import EventModel


def init_database(client: Client):
    client.execute(
        "CREATE DATABASE IF NOT EXISTS analytics ON CLUSTER company_cluster"
    )

    client.execute(
        """
        CREATE TABLE IF NOT EXISTS analytics.views ON CLUSTER company_cluster
            (
                id String
                user_id String,
                movie_id String,
                movie_progress Int32, # вохможно нужно заменить на другое название колонки
                event_type String,
            )
            Engine=MergeTree()
        ORDER BY id
        """
    )


def save_to_clickhouse(client: Client, events: List[EventModel]):
    # TODO: после того, как Серега определит модели, нужно правильно прописать поля
    client.execute(
        """
        INSERT INTO analytics.views
            (
                        id,
                        user_id,
                        movie_id,
                        movie_progress,
                        event_type
            )
        VALUES
        """,
        (
            (
                event.user_id,
                event.movie_id,
                event.movie_progress,
                event.event_type,
            )
            for event in events
        ),
    )
