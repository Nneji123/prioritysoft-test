# Makefile for Django project

# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
MANAGE = $(PYTHON) manage.py

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  install           Install project dependencies"
	@echo "  check_db          Check if the PostgreSQL database is ready"
	@echo "  prepare_migrations Prepare migration directories and files"
	@echo "  makemigrations    Create new database migrations"
	@echo "  migrate           Apply database migrations"
	@echo "  createsuperuser   Create a superuser"
	@echo "  collectstatic     Collect static files"
	@echo "  runserver         Run the Django development server"
	@echo "  start             Start the development server"
	@echo "  test              Run tests"
	@echo "  lint              Run linting checks"

# Install project dependencies
install:
	$(PIP) install -r requirements.txt

# Check if the PostgreSQL database is ready
check_db:
	if [ "$$ENVIRONMENT" = "Prod" ]; then \
		echo "Waiting for PostgreSQL..."; \
		if [ -z "$$DB_HOST" ]; then \
			DB_HOST="postgres"; \
		fi; \
		while ! nc -z $$DB_HOST 5432; do \
			sleep 1; \
		done; \
		echo "PostgreSQL is up and running."; \
	else \
		echo "Skipping PostgreSQL check as ENVIRONMENT is not set to Prod."; \
		if [ ! -d "logs" ]; then \
			mkdir -p logs; \
		fi; \
	fi

# Prepare migration directories and files
prepare_migrations:
	for dir in accounts core forum inventory; do \
		mkdir -p apps/$$dir/migrations && touch apps/$$dir/migrations/__init__.py; \
	done

# Create new database migrations
makemigrations:
	$(MANAGE) makemigrations

# Apply database migrations
migrate: check_db prepare_migrations
	$(MANAGE) migrate --run-syncdb

# Create a superuser
createsuperuser:
	$(MANAGE) customcreatesuperuser

# Collect static files
collectstatic:
	$(MANAGE) collectstatic --no-post-process --no-input

# Run the Django development server
runserver:
	$(MANAGE) runserver

# Start the development server
start: install migrate createsuperuser collectstatic runserver

# Run tests
test:
	DJANGO_SETTINGS_MODULE=backend.settings.development pytest tests --cov=apps --cov-report=xml

# Run linting checks
lint:
	black .
	isort .
