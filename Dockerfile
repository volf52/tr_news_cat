FROM python:3.8.6-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # tini
  TINI_VERSION=v0.19.0 \
  # poetry
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"

WORKDIR "/app"

RUN apt-get update && apt-get install --no-install-recommends -y wget curl bash build-essential git \
    && wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
    && chmod +x /usr/local/bin/tini && tini --version \
    && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
    && poetry --version \
    && apt-get remove -y wget && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && groupadd -r web && useradd -d /app -r -g web web \
    && chown web:web -R /app

# ---- Stage 2: Install Requirements --------------------------------------------

FROM base as reqinstall

COPY --chown=web:web ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-ansi --no-interaction && rm -rf "$POETRY_CACHE_DIR"

# ---- Stage 3: Install Application and get models ------------------------------

FROM reqinstall

ENV PORT=8080
ENV NWORKERS=2
ENV NTHREADS=8
ENV WORKER=uvicorn.workers.UvicornWorker

COPY --chown=web . /app/

# To install news_cat
RUN poetry install --no-ansi --no-interaction && rm -rf "$POETRY_CACHE_DIR" \
  && dvc pull && ls artifacts \
  && rm -rf .dvc && rm -rf .git

EXPOSE $PORT
USER web

ENTRYPOINT ["tini", "-g", "--"]

CMD gunicorn -b :${PORT} --threads ${NTHREADS} -w ${NWORKERS} -k ${WORKER} app:app