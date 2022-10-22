__all__ = (
    'CREATE_DB',
    'CREATE_TABLE',
    'INSERT_VALUES',
)

CREATE_DB = "CREATE DATABASE IF NOT EXISTS %s ON CLUSTER company_cluster"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS %s.%s ON CLUSTER company_cluster
   (
       event_name String,
       movie_id String,
       user_id String,
       event_data String,
       timestamp String
   )
   Engine=MergeTree()
ORDER BY timestamp"""

INSERT_VALUES = f"INSERT INTO %s.%s VALUES"
