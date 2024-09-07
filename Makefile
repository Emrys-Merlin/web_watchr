SHELL := /bin/bash

.PHONY: setup
setup:
	pip install uv
	uv pip install -e ".[dev,docs]"
	pre-commit install

.PHONY: test
test:
	pytest --cov=web_watchr --cov-report term-missing

.PHONY: setup-ci
run-ci:
	pip install --upgrade pip
	pip install uv
	uv venv
	uv pip install -e ".[dev]"
	uv run pytest --cov=web_watchr --cov-report term-missing --cov-report xml:coverage.xml --junit-xml=report.xml

.PHONY: docs
docs:
	mkdocs gh-deploy
