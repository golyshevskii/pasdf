DT_NOW := $(shell date)

poetry-install:
	@$(info INFO | $(shell date) | Makefile → poetry-install)
	poetry install

format:
	@$(info INFO | $(shell date) | Makefile → format)
	poetry run black .
	poetry run isort .
	poetry run flake8 .

lint:
	poetry run black --check .
	poetry run isort --check .

.PHONY: tests

tests:
	@$(info INFO | $(shell date) | Makefile → tests)
	pytest tests -v

test-coverage:
	@echo 'Running test coverage with arguments: '$(pytest-args)
	pytest tests --cov=. --cov-report=term-missing --cov-config=../pyproject.toml -c ../pyproject.toml .
