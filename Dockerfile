FROM apache/airflow:2.6.3-python3.11

RUN pip install --upgrade pip pytest

USER root
RUN apt-get update -y \
  # dependencies for building Python packages
  && apt-get install -y build-essential libxml2-dev libxmlsec1-dev \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Git dependencies
  && apt-get install git openssh-client -y \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

USER airflow

# RUN pip install --no-cache-dir --upgrade pip setuptools poetry poetry-core

# COPY pyproject.toml poetry.lock /

# RUN poetry config virtualenvs.create false && \
#     poetry install --no-interaction --no-ansi
