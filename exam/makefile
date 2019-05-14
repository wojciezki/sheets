HOST=127.0.0.1
TEST_PATH=./sheets/

clean-pyc:
    find . -name '*.pyc' -exec rm --force {} +
    find . -name '*.pyo' -exec rm --force {} +
   name '*~' -exec rm --force  {}

clean-build:
    rm --force --recursive build/
    rm --force --recursive dist/
    rm --force --recursive *.egg-info


isort:
    sh -c "isort --skip-glob=.tox --recursive . "

lint:
    flake8 --exclude=.tox

test: clean-pyc
    py.test --verbose --color=yes $(TEST_PATH)

run:
    python3.6 -m venv venv_sheets
    activate venv_sheets/bin/activate
    pip install -r requirements.txt
    python manage.py loaddata base.json
    python manage.py runserver