
FROM python:3.9-slim-bullseye AS builder

WORKDIR /app

ADD pyproject.toml poetry.lock /app/

RUN apk add build-base libffi-dev

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi

FROM python:3.9-slim-bullseye
WORKDIR /app

COPY --from=builder /app /app
ADD . /app

# Create a new group `app` with Group ID `1000`.
RUN addgroup --gid 1000 django
# Create a new user `app`, sets home directory to `/app`, User ID `1000`, in
# the group `app`. The `-DH` option results in a system account.
RUN adduser django -h /app -u 1000 -G django -DH
# Change the user for subsequent commands in Dockerfile to the user with ID
# `1000`.
USER 1000

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

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start


ENTRYPOINT ["/entrypoint"]
CMD ${STARTUP_COMMAND}
