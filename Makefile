.DEFAULT_GOAL := help

.PHONY: help
help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: init-pre-commit
init-pre-commit: ## Init pre-commit.
	@pre-commit install
	@pre-commit install --hook-type commit-msg

.PHONY: tests
test: ## Run tests.
	@pytest -vv
	@mypy

.PHONY: lint
lint: ## Check linter.
	@pre-commit run --all-files

.PHONY: coverage-html
coverage-html: ## Run pytest with html output coverage.
	@pytest --cov-report html

.PHONY: ci
ci: lint test ## Run CI.

.PHONY: bump-version
bump-version: check-version ## Bump version, define target version with "VERSION=*.*.*".
	@sed -i "s/^\(version = \"\)\(.\)*\"/\1${VERSION}\"/" pyproject.toml
	@echo "Version replaced by ${VERSION} in 'pyproject.toml'"

check-version:
ifndef VERSION
	$(error VERSION is undefined)
endif
