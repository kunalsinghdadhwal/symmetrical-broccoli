.PHONY: dev test ingest lint format typecheck

dev:
	pip install -e ".[dev]"

test:
	pytest tests/

ingest:
	python -m src.ingest.pipeline

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/
