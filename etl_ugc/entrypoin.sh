#!/bin/sh

echo "Waiting for Kafka..."
while ! nc -z -v $KAFKA_HOST $KAFKA_PORT;
do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 0.4;
done
echo "KAFKA was started"

echo "Waiting for Clickhouse..."
while ! nc -z -v $CH_HOST $CH_PORT;
do
  >&2 echo "Clickhouse is unavailable - sleeping"
  sleep 0.4;
done
echo "Clickhouse was started"

exec "$@"