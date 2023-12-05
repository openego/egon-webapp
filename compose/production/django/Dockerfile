# define an alias for the specific python version used in this file.
FROM python:3.11.6-slim-bullseye as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # git \
  git

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential binutils libproj-dev gdal-bin \
  apt-transport-https \
  git \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # Only for django-distill (remove later)
  ca-certificates \
  && update-ca-certificates \
  # Locales de-De
  && apt-get install -y locales \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE:en
ENV LC_ALL de_DE.UTF-8

# install requirements
COPY ./pyproject.toml ./poetry.lock ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir poetry && poetry install --no-root
# Move this into poetry file, once changes merged into pypi package
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-distill.git@djagora
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-raster.git@djagora

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

# copy application code to WORKDIR
COPY --chown=django:django . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]
