# Scylla Docker
up:
	docker-compose up -d
down:
	docker-compose down
stop:
	docker-compose stop
buildimage:
	docker-compose build


# ScyllaDB
cqlsh:
	docker exec -it $$(docker-compose ps -q node1) cqlsh

logs:
	docker logs $$(docker-compose ps -q node1) | tail

status:
	docker exec -it $$(docker-compose ps -q node1) nodetool status

app:
	docker exec -it $$(docker-compose ps -q app) bash

restart:
	docker exec -it $$(docker-compose ps -q node1) supervisorctl restart scylla

info:
	docker exec -it $$(docker-compose ps -q node1) nodetool describecluster

# Python Build
build: lint check_types test

lint:
	poetry run flake8

check_types:
	poetry run mypy .

test:
	poetry run pytest