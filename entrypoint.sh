#!/bin/bash
set -e

# Ожидание PostgreSQL (если нужен)

echo "⏳ Ждём базу данных..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

# Применение миграций
echo "📦 Применяем миграции..."
alembic upgrade head

# Запуск приложения
echo "🚀 Запуск приложения..."
exec "$@"