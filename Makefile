.PHONY: setup
setup:	
	pip install uv
	uv pip install -e ".[dev]"

.PHONY: test
test:
	pytest --cov=web_watchr --cov-report term-missing
