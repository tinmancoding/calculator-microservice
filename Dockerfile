FROM python:3.12-bookworm as builder
ARG APP_NAME

RUN pip install --no-cache-dir poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /
COPY calc-common/ ./calc-common/

WORKDIR /app

COPY calc-${APP_NAME}/pyproject.toml calc-${APP_NAME}/poetry.lock ./
RUN touch README.md

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-slim-bookworm as runtime
ARG APP_NAME

ENV VIRTUAL_ENV=/app/.venv \
  PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /calc-common /calc-common


COPY calc-${APP_NAME}/calc_${APP_NAME} calc_${APP_NAME}

ENV APP_MAIN=calc_${APP_NAME}/main.py
ENV APP_PORT=8000

ENTRYPOINT ["sh", "-c", "fastapi run ${APP_MAIN} --port ${APP_PORT}"]
