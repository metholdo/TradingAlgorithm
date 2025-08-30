
.PHONY: setup lint test run

setup:
	uv sync

lint:
	ruff check .
	black --check .
	mypy .

test:
	pytest -q

run:
	uv run trader --help
