#!/bin/bash
set -e

echo "⏳ Waiting for DB"
until pg_isready -h "$BOT_DB_HOST" -p "$BOT_DB_PORT" -U "$BOT_DB_USER"; do
  sleep 1
done
echo "📦 Applying migrations"
alembic upgrade head

echo "🚀 Start App"
exec "$@"