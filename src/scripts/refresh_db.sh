#!/bin/bash

export $(grep '^DATABASE_' .env | tr -d '\r' | xargs)

docker compose exec postgres psql postgresql://$DATABASE_USER:$DATABASE_PASSWORD@localhost/$DATABASE_DATABASE -c \
    'DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;'

echo ""
./src/scripts/alembic.sh upgrade head
# docker compose exec python uv run ../scripts/populate_db.py
