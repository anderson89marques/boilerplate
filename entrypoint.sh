#!/bin/sh
make migrate
poetry run uvicorn --host 0.0.0.0 src.app:app