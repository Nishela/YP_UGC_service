from reserch.config import get_settings

settings = get_settings()

TABLE = settings.clickhouse.table
INSERT_QUERY = """INSERT INTO movies.views VALUES"""

SELECT_QUERIES = {
    "unique_user_exact": f"select uniqExact(user_id) from {TABLE}",
    "unique_movies_exact": f"select uniqExact(movie_id) from {TABLE}",
    "unique_movies_count": f"select count(distinct movie_id) from {TABLE}",
    "unique_users_count": f"select count(distinct user_id) from {TABLE}",
    "user_stat": f"SELECT user_id, sum(event_data), max(event_data)\
     FROM {TABLE} GROUP by user_id"
}