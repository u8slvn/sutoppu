.PHONY: help tests quality coverage coverage-html

.DEFAULT_GOAL := help

help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install package locally with dependencies.
	@pip install -e .

install-dev: ## Install package locally with dev dependencies.
	@pip install -e .\[dev\]

tests: ## Run tests.
	@pytest tests/ -x -vv

quality: ## Check quality.
	@flake8
	@bandit -r sutoppu/

coverage: ## Run tests with coverage.
	@pytest tests/ --cov=sutoppu

coverage-html: ## Run tests with html output coverage.
	@pytest tests/ --cov=sutoppu --cov-report html

ci: quality coverage ## Run CI.
