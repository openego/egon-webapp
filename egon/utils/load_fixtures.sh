#!/usr/bin/env bash

# Execute this script in your project root folder with activated virtualenv:
#
# $ bash egon/utils/load_fixture.sh

set -e

python manage.py loaddata egon/map/fixtures/region.json
python manage.py loaddata egon/map/fixtures/district.json

python manage.py loaddata egon/map/fixtures/cluster.json
python manage.py loaddata egon/map/fixtures/nightlight.json
python manage.py loaddata egon/map/fixtures/hospitals.json
python manage.py loaddata egon/map/fixtures/hospitalssimulated.json
