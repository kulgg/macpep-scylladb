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
	docker exec -it $$(docker-compose ps -q node1) watch -n 0.5 nodetool status macpep

app:
	docker exec -it $$(docker-compose ps -q app) bash

restart:
	docker exec -it $$(docker-compose ps -q node1) supervisorctl restart scylla

info:
	docker exec -it $$(docker-compose ps -q node1) nodetool describecluster

# Python Build
build: lint test

lint:
	poetry run flake8
test:
	poetry run pytest