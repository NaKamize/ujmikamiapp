#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

if [ "$PRODUCTION" != "true" ]; then
    echo "Running seeders (development mode)..."
    python manage.py seed_ml_models
    python manage.py seed_projects
    python manage.py seed_publications
    python manage.py seed_experiences
    python manage.py seed_aboutme
fi

if [ "$PRODUCTION" = "true" ]; then
    echo "Starting Gunicorn..."
    exec gunicorn --bind 0.0.0.0:8000 ujmikamiapp.wsgi:application
else
    echo "Starting Development Server..."
    exec python manage.py runserver 0.0.0.0:8000
fi