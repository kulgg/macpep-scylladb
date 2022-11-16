start:
	docker-compose up -d

stop:
	docker-compose stop

down:
	docker-compose down

# ScyllaDB
cqlsh:
	docker exec -it $$(docker-compose ps -q $(node)) cqlsh

logs:
	docker logs $$(docker-compose ps -q node1) | tail

status:
	for i in 1 2 3; do docker exec -it $$(docker-compose ps -q node$$i) nodetool status; done

restart:
	docker exec -it $$(docker-compose ps -q node1) supervisorctl restart scylla

info:
	docker exec -it $$(docker-compose ps -q node1) nodetool describecluster
