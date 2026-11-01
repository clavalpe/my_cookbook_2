#!/usr/bin/make -f

.DEFAULT_GOAL := help

.PHONY: test linting build
.PHONY: env-start env-stop env-recreate docker-cleanup migrations migrate bash shell url wait-db
.PHONY: pr changelog prepare-deploy view-logs help

ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(ROOT_FOLDER)/docker/docker-compose.yml
PROJECT_NAME ?= my-cookbook-$(notdir $(ROOT_FOLDER))

ALEMBIC_CONFIG := /app/alembic.ini
DOCKER_COMMAND := docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE)

test:
	$(DOCKER_COMMAND) exec -T app pytest .

linting: check-style check-format check-types

check-style:
	$(DOCKER_COMMAND) exec -T app ruff check .

check-format:
	$(DOCKER_COMMAND) exec -T app ruff format --check .

check-types:
	$(DOCKER_COMMAND) exec -T app mypy .

fix-linting: fix-format fix-style

fix-style:
	$(DOCKER_COMMAND) exec -T app ruff check --fix .

fix-format:
	$(DOCKER_COMMAND) exec -T app ruff format .

build:
	$(DOCKER_COMMAND) build --no-cache

env-start:
	$(DOCKER_COMMAND) up -d --build

wait-db: ## Blocks until the database accepts connections
	$(DOCKER_COMMAND) exec -T db sh -c 'until pg_isready; do sleep 1; done'

url: ## Prints the host address where the app of this checkout is published
	@$(DOCKER_COMMAND) port app 8000

env-stop:
	$(DOCKER_COMMAND) stop

env-restart: env-stop env-start

env-destroy:
	$(DOCKER_COMMAND) down -v --rmi all --remove-orphans

env-recreate: build env-start

env-reset: destroy-containers env-start

destroy-containers:
	$(DOCKER_COMMAND) down -v

docker-cleanup:
	$(DOCKER_COMMAND) down -v
	docker system prune -f

migrations: ## Creates new alembic revision
	$(DOCKER_COMMAND) exec -T app alembic -c $(ALEMBIC_CONFIG) revision --autogenerate

migrate: ## Applies the alembic revisions up to head
	$(DOCKER_COMMAND) exec -T app alembic -c $(ALEMBIC_CONFIG) upgrade head

bash: ## Open a bash shell in project's main container
	$(DOCKER_COMMAND) exec app bash

shell: ## Open a FastAPI shell in project's main container
	$(DOCKER_COMMAND) exec app python -i app.py


