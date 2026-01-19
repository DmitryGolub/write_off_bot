FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --no-interaction --no-ansi

COPY app/ ./app/
COPY alembic.ini ./
COPY alembic/ ./alembic/

RUN mkdir -p .data/images

COPY .data/ ./.data/

CMD ["python", "-m", "app.main"]
