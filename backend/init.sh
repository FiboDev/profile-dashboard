#!/bin/bash
set -e

echo "🚀 Starting application initialization..."

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Seed database if in development mode or if SEED_DATABASE is set
if [ "${ENVIRONMENT:-development}" = "development" ] || [ "${SEED_DATABASE:-false}" = "true" ]; then
    echo "🌱 Seeding database with sample data..."
    python database/seeder.py
else
    echo "⏭️  Skipping database seeding (not in development mode)"
fi

echo "✅ Application initialization completed!"

# Start the application
echo "🚀 Starting FastAPI server..."
exec "$@"
