FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install gcc g++ make -y

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
