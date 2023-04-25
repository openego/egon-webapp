
.PHONY : load_regions load_data empty_data dump_fixtures load_fixtures distill

DISTILL=True
export

load_regions:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.load_regions()"

load_data:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.load_data()"

load_csv:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.load_csv()"

load_raster:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.load_raster()"

build_clusters:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.build_cluster_geojson()"

empty_regions:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.empty_data(data_models=data_processing.REGIONS)"

empty_data:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.empty_data()"

empty_raster:
	python manage.py shell --command="from egon.utils import data_processing; data_processing.empty_raster()"

dump_fixtures:
	bash egon/utils/dump_fixtures.sh

load_fixtures:
	bash egon/utils/load_fixtures.sh

distill:
	python manage.py distill-local --force --exclude-staticfiles ./egon/static/mvts

check_distill_coordinates:
	python manage.py shell --command="from egon.utils import distill; print(distill.check_distill_coordinates())"


local_env_file:
	python merge_local_dotenvs_in_dotenv.py
