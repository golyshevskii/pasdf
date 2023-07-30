DT_NOW := $(shell date) 

poetry-install:
	@$(info INFO | $(shell date) | Makefile → poetry-install)
	poetry install

format:
	@$(info INFO | $(shell date) | Makefile → format)
	poetry run black .
	poetry run isort .
	poetry run flake8 .
