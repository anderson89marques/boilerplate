run:
	hypercorn src.app:app

test:
	pytest -svv

test-matching:
	pytest -svv -k=$(K)