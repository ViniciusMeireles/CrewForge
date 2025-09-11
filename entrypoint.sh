#!/bin/sh

set -o errexit
set -o nounset

# Wait for PostgreSQL
counter=0
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "PostgreSQL is not available - waiting..."
  sleep 2
  counter=$((counter+1))
  if [ $counter -gt 30 ]; then
    >&2 echo "Timeout waiting for PostgreSQL"
    exit 1
  fi
done

echo "PostgreSQL is available :D - continuing..."

exec "$@"
