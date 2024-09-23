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
setup-ci:
	pip install --upgrade pip
	pip install uv
	uv venv
	uv pip install -e ".[dev]"

.PHONY: run-ci
run-ci: setup-ci
	uv run pytest --cov=web_watchr --cov-report term-missing --cov-report xml:coverage.xml --junit-xml=report.xml

.PHONY: docs
docs:
	mkdocs gh-deploy

.PHONY: clean
clean:
	rm -rf site
	rm -rf dist

.PHONY: build
build:
	uv build

# Needs different credentials
# .PHONY: publish-test
# publish-test:
# 	uvx twine upload --repository testpypi dist/*

.PHONY: publish
publish:
	uvx twine upload dist/*
