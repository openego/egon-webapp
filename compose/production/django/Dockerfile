# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"
ARG APP_HOME="/app"
ARG BUILD_ENVIRONMENT=production


FROM python:3.11.6-slim-bullseye AS builder

# Renew (https://stackoverflow.com/a/53682110):
ARG WORKDIR

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # git \
  git

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR ${WORKDIR}
COPY . .

RUN poetry install --only main

FROM python:3.11.6-slim-bullseye

ARG WORKDIR
WORKDIR ${WORKDIR}
COPY --from=builder ${WORKDIR} .

# For options, see https://boxmatrix.info/wiki/Property:adduser

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  git \
  # Geospatioal dependencies
  binutils libproj-dev gdal-bin \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Move this into poetry file, once changes merged into pypi package
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-distill.git@djagora
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-raster.git@djagora

RUN pip install psycopg2-binary

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start

# copy application code to WORKDIR
COPY --chown=django:django . ${WORKDIR}

# make django owner of the WORKDIR directory as well.
RUN chown -R django:django ${WORKDIR}

USER django

ENTRYPOINT ["/entrypoint"]
CMD ${STARTUP_COMMAND}
