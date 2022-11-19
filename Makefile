start:
	docker-compose up -d

stop:
	docker-compose stop

# ScyllaDB
cqlsh:
	docker exec -it $$(docker-compose ps -q node1) cqlsh

logs:
	docker logs $$(docker-compose ps -q node1) | tail

status:
	docker exec -it $$(docker-compose ps -q node1) nodetool status

restart:
	docker exec -it $$(docker-compose ps -q node1) supervisorctl restart scylla

info:
	docker exec -it $$(docker-compose ps -q node1) nodetool describecluster

build: lint check_types test

lint:
	poetry run flake8

check_types:
	poetry run mypy .

test:
	poetry run pytest
