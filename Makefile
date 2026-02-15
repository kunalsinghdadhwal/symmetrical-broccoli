.PHONY: dev test ingest

dev:
	pip install -e ".[dev]"

test:
	pytest tests/

ingest:
	python -m src.ingest.pipeline
