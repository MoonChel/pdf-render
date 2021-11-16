.PHONY: run

run:
	docker-compose up --build -d db
	docker-compose run api alembic upgrade head
	docker-compose up --build api worker

tests:
	docker-compose up --build -d test_db
	docker-compose build api
	docker-compose run -e DATABASE_HOST=test_db api pytest
	docker-compose stop

clear:
	docker-compose rm