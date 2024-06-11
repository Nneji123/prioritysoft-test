#!/bin/sh

# THIS SCRIPT IS FOR RENDER DEPLOYMENT

set -e

# Wait for the database to be ready if in production mode
if [ "$SERVER_MODE" != "Prod" ]; then
  echo "Skipping PostgreSQL check as SERVER_MODE is not set to Prod."
  if [ ! -d "data/backup" ]; then
    mkdir -p data/backup
  fi
  if [ ! -d "logs" ]; then
    mkdir -p logs
  fi
else
  echo "Waiting for PostgreSQL..."
  if [ -z "$DB_HOST" ]; then
    # Default to 'postgres' if DB_HOST is not defined
    DB_HOST="postgres"
  fi

  while ! nc -z $DB_HOST 5432; do
    sleep 1
  done

  echo "PostgreSQL is up and running."
fi

# Make sure the migrations directories and __init__.py files exist
for dir in userauth core forum gamification tracking edumaterials telehealth; do
    mkdir -p apps/$dir/migrations && touch apps/$dir/migrations/__init__.py
done

# Run migrations
python manage.py makemigrations
python manage.py migrate --run-syncdb

# Create superuser
python manage.py customcreatesuperuser

# Collect static files
python manage.py collectstatic --no-post-process --no-input --upload-unhashed-files

celery -A backend beat -l info --detach && celery -A backend worker -l info --detach && gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --env DJANGO_CONFIGURATION=DevConfig
