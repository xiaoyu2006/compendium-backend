FROM python:3.12.4-slim-bookworm


ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt-get update && apt-get upgrade && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN /opt/poetry/bin/poetry install --without dev

COPY . .

CMD [ "/opt/poetry/bin/poetry", "run", "fastapi", "run", "main.py" ]

