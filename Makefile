# Makefile for Django project

# Variables
PYTHON = python
PIP = $(PYTHON) -m  pip
MANAGE = $(PYTHON) manage.py

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Available targets:"
	@echo "  install           Install project dependencies"
	@echo "  migrate           Apply database migrations"
	@echo "  createsuperuser   Create a superuser"
	@echo "  runserver         Run the Django development server"
	@echo "  test              Run tests"
	@echo "  lint              Run linting checks"

# Install project dependencies
install:
	$(PIP) install -r requirements.txt

# Apply database migrations
migrate:
	$(MANAGE) migrate

# Create a superuser
createsuperuser:
	$(MANAGE) createsuperuser

# Run the Django development server
runserver:
	$(MANAGE) runserver

# Run tests
test:
	pytest test --cov=apps --cov-report=xml

# Run linting checks
lint:
	black .
 isort .
