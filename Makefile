install:
	poetry install --no-dev

install_dev:
	poetry install

lint:
	poetry run task lint

format:
	poetry run task format