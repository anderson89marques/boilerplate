SHELL=/bin/bash

run:
	poetry run uvicorn --host 0.0.0.0 src.app:app

test:
	pytest -svv

test-matching:
	pytest -svv -k=$(K)

lint:
	ruff check . && blue --check . --diff && isort --check . --diff 

format:
	blue .  && isort .	

migration:
	@alembic revision --autogenerate -m $(name)

migrate:
	@alembic upgrade head
