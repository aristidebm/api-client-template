install:
	poetry install  --no-dev

install_dev:
	poetry install

codestyle:
	ruff -v check src
	black --check src