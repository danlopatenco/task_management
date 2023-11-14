#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Load environment variables from .envrc
echo "Sourcing environment variables from .envrc"
source /app/.envrc

# Run the command passed to the entrypoint
exec "$@"