DROP_TABLE = "DROP TABLE IF EXISTS events"

CREATE_TABLE = """
                CREATE TABLE IF NOT EXISTS events (
                id           UUID      DEFAULT UUID_GENERATE(),
                event_name   VARCHAR   NOT NULL,
                user_id      UUID      NOT NULL,
                movie_id     UUID      NOT NULL,
                event_data   VARCHAR   NOT NULL,
                timestamp    TIMESTAMP NOT NULL)
"""

INSERT_VALUES = """
INSERT INTO events (event_name, user_id, movie_id, event_data, timestamp) VALUES (%s,%s,%s,%s,%s)
"""

SELECT_QUERIES = {
    "unique_user_exact": "select distinct user_id from events",
    "unique_movies_exact": "select distinct movie_id from events",
    "unique_movies_count": "select count(distinct movie_id) from events",
    "unique_users_count": "select count(distinct user_id) from events",
    "user_stat": "SELECT user_id, sum(event_data), max(event_data) FROM events GROUP by user_id"
}
