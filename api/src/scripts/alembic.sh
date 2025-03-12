#!/bin/bash

ALL_ARGS=("$@")
docker compose exec -w /app/src api alembic "$@"
