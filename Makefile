
load_data:
	python manage.py shell --command="from enershelf.utils import data_processing; data_processing.load_data()"

empty_data:
	python manage.py shell --command="from enershelf.utils import data_processing; data_processing.empty_data()"
