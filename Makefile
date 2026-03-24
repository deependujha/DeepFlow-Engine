.PHONY: test test-verbose test-cov test-fast lint format clean install-dev

install-dev:
	uv sync --group dev

test:
	uv run pytest

test-verbose:
	uv run pytest -v

test-cov:
	uv run pytest --cov=src/deepflow_engine --cov-report=html --cov-report=term-missing

test-fast:
	uv run pytest -n auto

test-unit:
	uv run pytest tests/unit -v

test-integration:
	uv run pytest tests/integration -v

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type d -name htmlcov -exec rm -rf {} +
	find . -type f -name .coverage -delete

release:
	chmod +x scripts/bump_version.sh
	./scripts/bump_version.sh
