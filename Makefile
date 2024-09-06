.PHONY: setup
setup:
	pip install uv
	uv pip install -e ".[dev]"
	pre-commit install

.PHONY: test
test:
	pytest --cov=web_watchr --cov-report term-missing
