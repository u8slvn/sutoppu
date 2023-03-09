.PHONY: help tests quality coverage coverage-html

.DEFAULT_GOAL := help

help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

tests: ## Run tests.
	@poetry run pytest tests/ -x -vv
	@poetry run mypy sutoppu.py

quality: ## Check quality.
	@poetry run flake8
	@poetry run black --check sutoppu.py

format: ## Format files.
	@poetry run black sutoppu.py

coverage: ## Run tests with coverage.
	@poetry run pytest tests/ --cov=sutoppu

coverage-html: ## Run tests with html output coverage.
	@poetry run pytest tests/ --cov=sutoppu --cov-report html

ci: quality coverage ## Run CI.
