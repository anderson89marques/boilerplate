SHELL=/bin/bash

run:
	hypercorn src.app:app

test:
	pytest -svv

test-matching:
	pytest -svv -k=$(K)

lint:
	ruff check . && blue --check . --diff && isort --check . --diff 

format:
	blue .  && isort . 
