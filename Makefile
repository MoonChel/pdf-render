.PHONY: run

run:
	docker-compose up --build

tests:
	docker-compose up --build -d test_db
	docker-compose up --build test_api
	docker-compose stop
