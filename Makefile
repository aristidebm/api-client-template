install:
	poetry install --no-dev

install_dev:
	poetry install

codestyle:
	poetry run task lint
	poetry run task format