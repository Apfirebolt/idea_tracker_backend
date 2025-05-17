#!/bin/bash

echo "Starting entrypoint script..."

echo "Running Alembic migrations..."
python -m alembic upgrade head
echo "Alembic migrations finished."

echo "Starting Uvicorn server..."
exec uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000
echo "This line should not be printed if Uvicorn starts correctly."