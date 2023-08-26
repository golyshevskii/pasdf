DT_NOW := $(shell date)
DC := docker compose

poetry-install:
	@$(info INFO | $(shell date) | Makefile → poetry-install)
	poetry install

poetry-update:
	@$(info INFO | $(shell date) | Makefile → poetry-install)
	poetry update

format:
	@$(info INFO | $(shell date) | Makefile → format)
	poetry run black .
	poetry run isort .
	poetry run flake8 .

lint:
	@$(info INFO | $(shell date) | Makefile → lint)
	poetry run black --check .
	poetry run isort --check .
	poetry run flake8 .

.PHONY: tests

tests:
	@$(info INFO | $(shell date) | Makefile → tests)
	pytest main/tests -v

test-coverage:
	@$(info INFO | $(shell date) | Makefile → test-coverage)
	pytest main/tests --cov=. --cov-report=term-missing --cov-config=./pyproject.toml -c ./pyproject.toml .

setup:
	@$(info INFO | $(shell date) | Makefile → setup)
	cp docker-compose-example.yaml docker-compose.yaml
	mkdir -p ./logs ./plugins

	make airflow-init
	make up

airflow-init:
	@$(info INFO | $(shell date) | Makefile → airflow-init)
	$(DC) up airflow-init

up:
	@$(info INFO | $(shell date) | Makefile → up)
	$(DC) up -d --build

down:
	@$(info INFO | $(shell date) | Makefile → down)
	$(DC) down

build:
	@$(info INFO | $(shell date) | Makefile → build)
	$(DC) build --no-cache


# WARNING: Delete all docker cashed files
prune:
	@$(info INFO | $(shell date) | Makefile → prune)
	docker system prune
