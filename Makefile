# Makefile for Django/Docker operations

.PHONY: help build up down logs uv_add uv_upgrade makemigrations migrate createsuperuser shell_plus spectacular format_code test precommit

DEFAULT_GOAL := help

help:  ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ General

build:  ## Build Docker images
	docker compose build --no-cache

up:  ## Start containers in background mode
	docker compose up -d

down:  ## Stop and remove containers
	docker compose down --remove-orphans

logs:  ## Show django_api container logs
	docker compose logs -f django_api

uv_add:  ## Add a new library to the uv project
	@if [ -z "$(lib)" ]; then \
		echo "Error: lib variable is not set. Usage: make uv_add lib=<library_name>"; \
		exit 1; \
	fi
	docker compose exec django_api uv add $$lib

uv_upgrade:  ## Upgrade all libraries in the uv project
	docker compose exec django_api uv sync --upgrade


##@ Development

makemigrations:  ## Make migrations for the Django project
	docker compose exec django_api uv run python manage.py makemigrations

migrate:  ## Apply migrations for the Django project
	docker compose exec django_api uv run python manage.py migrate

createsuperuser:  ## Create a superuser for the Django project
	docker compose exec django_api uv run python manage.py createsuperuser

shell_plus:  ## Open Django shell with all models imported
	docker compose exec django_api uv run python manage.py shell_plus

spectacular:  ## Generate OpenAPI schema for the Django project
	docker compose exec django_api uv run python manage.py spectacular --color --file schema.yml

format_code:  ## Format code with black
	docker compose exec django_api uv run black .
	docker compose exec django_api uv run isort .

test:  ## Run tests for the Django project
	docker compose exec django_api uv run python manage.py test

precommit: format_code spectacular test  ## Run code formatting and tests
	@echo "Pre-commit checks passed."
