run-ingest:
	docker-compose up ingest

run-worker:
	docker-compose up worker

run-all:
	docker-compose up

build:
	docker-compose build

logs:
	docker-compose logs -f

clean:
	docker-compose down -v