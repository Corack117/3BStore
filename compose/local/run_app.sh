#!/bin/bash

# Script to wait for database services and run Django commands

# Wait for PostgreSQL to be available
/wait-for-it.sh postgres_db:5432 --timeout=60 --strict -- echo "PostgreSQL is up"

# Run Django management commands
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
