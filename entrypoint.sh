#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
python manage.py migrate

# Start the server
exec "$@"
