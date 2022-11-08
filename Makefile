THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-api ps login-timesc

help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

run:
	docker-compose -f docker-compose.yml up -d --build

run_m1:
	docker-compose -f docker-compose_m1.yml up -d --build

run_and_config_mongo:
	docker-compose -f docker-compose-mongo.yml up -d --build && chmod +x ./mongo_setup.sh && sh ./mongo_setup.sh

delete:
	docker-compose down -v $(c)

etl_logs:
	docker-compose logs etl-ugc --tail=100

ugc_logs:
	docker-compose logs ugc-service --tail=100