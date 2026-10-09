#!/bin/sh
set -e
alembic upgrade head
if [ "$SEED_ON_START" = "true" ]; then
  python -m app.db.seed
fi
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
