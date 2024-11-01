SHELL := /bin/bash

.PHONY: setup
setup:
	uv sync
	uv run pre-commit install

.PHONY: test
test:
	uv run pytest --cov=web_watchr --cov-report term-missing

.PHONY: setup-ci
setup-ci:
	uv sync

.PHONY: run-ci
run-ci: setup-ci
	uv run pytest --cov=web_watchr --cov-report term-missing --cov-report xml:coverage.xml --junit-xml=report.xml

.PHONY: docs
docs:
	uv run mkdocs gh-deploy

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
	uv publish
