(PYTHON_VERSION)=/usr/bin/python3.6

test:
	python manage.py test

install:
	virtualenv --python=$(PYTHON_VERSION) venv_sheets
	. venv_sheets/bin/activate
	pip install -r requirements.txt
	python manage.py migrate

run:
	python manage.py loaddata base.json
	python manage.py runserver
