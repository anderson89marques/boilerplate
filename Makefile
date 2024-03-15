run:
	hypercorn src.app:app

test:
	pytest -svv

test-matching:
	pytest -svv -k=$(K)

lint:
	ruff . && blue --check . --diff && isort --check . --diff 

format:
	blue .  && isort . 
