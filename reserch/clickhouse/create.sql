CREATE DATABASE IF NOT EXISTS movies ON CLUSTER 'company_cluster';

CREATE TABLE IF NOT EXISTS movies.views ON CLUSTER 'company_cluster' (
    id           UUID,
    event_name   String,
    movie_id     UUID,
    user_id      UUID,
    event_data   INTEGER,
    timestamp    DateTime
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/table', '{replica}')
PARTITION BY toDateTime(timestamp)
ORDER BY (id);

CREATE TABLE IF NOT EXISTS movies.views_distr ON CLUSTER 'company_cluster' AS movies.views
ENGINE = Distributed('company_cluster', movies, views, id);