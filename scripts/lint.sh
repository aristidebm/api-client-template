set -e
set -x

ruff check src
black --check src
isort --check-only src