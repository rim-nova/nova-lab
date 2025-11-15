#!/bin/bash

echo "Starting InfinityInsight Backend..."

# Wait for database to be ready
if [ -n "$POSTGRES_HOST" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $POSTGRES_HOST 5432; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Run migrations (if using alembic)
# alembic upgrade head

# Start application
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
