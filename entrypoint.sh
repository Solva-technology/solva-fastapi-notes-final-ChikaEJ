#!/bin/sh
set -e

echo "Applying database migrations..."

retries=0
max_retries=30

until alembic upgrade head; do
  retries=$((retries+1))
  if [ "$retries" -ge "$max_retries" ]; then
    echo "Migrations failed after $max_retries attempts. Exiting."
    exit 1
  fi
  echo "Database not ready. Retrying ($retries/$max_retries) in 2s..."
  sleep 2
done

echo "Starting application..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000


