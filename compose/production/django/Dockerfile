# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"
ARG BUILD_ENVIRONMENT=production


FROM python:3.9-slim-bullseye AS builder

# Renew (https://stackoverflow.com/a/53682110):
ARG WORKDIR

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

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


WORKDIR ${WORKDIR}
COPY . .

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN pip install poetry && poetry config virtualenvs.create false
RUN poetry install --without dev

# Move this into poetry file, once changes merged into pypi package
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-distill.git@djagora
RUN pip install --trusted-host github.com git+https://github.com/henhuy/django-raster.git@djagora
RUN pip list

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY --chown=django:django . ${WORKDIR}

# make django owner of the WORKDIR directory as well.
RUN chown -R django:django ${WORKDIR}

USER django

ENTRYPOINT ["/entrypoint"]
CMD ${STARTUP_COMMAND}
