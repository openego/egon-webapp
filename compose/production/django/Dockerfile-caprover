
# Global ARG, available to all stages (if renewed)
FROM python:3.9-slim-bullseye AS builder
ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  git \
  build-essential \
  # Geospatioal dependencies
  binutils libproj-dev gdal-bin \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# copy application code to WORKDIR
COPY --chown=django:django . ${APP_HOME}



RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install --without dev

# Move this into poetry file, once changes merged into pypi package
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-distill.git@djagora
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-raster.git@djagora

COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY --chown=django:django . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

USER django

ENTRYPOINT ["/entrypoint"]

CMD ${STARTUP_COMMAND}
