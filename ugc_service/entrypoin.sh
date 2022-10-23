#!/bin/sh

echo "Waiting for Kafka..."
while ! nc -z -v $KAFKA_HOST $KAFKA_PORT;
do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 0.4;
done
echo "KAFKA was started"


exec "$@"