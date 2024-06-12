#!/bin/sh

set -e

# Wait for the database to be ready if in production mode
if [ "$ENVIRONMENT" != "Prod" ]; then
  echo "Skipping PostgreSQL check as ENVIRONMENT is not set to Prod."
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
for dir in accounts core inventory; do
    mkdir -p apps/$dir/migrations && touch apps/$dir/migrations/__init__.py
done

# Run migrations
python manage.py makemigrations
python manage.py migrate --run-syncdb

# Create superuser
python manage.py customcreatesuperuser

# Collect static files
python manage.py collectstatic --no-post-process --no-input

# Execute the CMD
exec "$@"
