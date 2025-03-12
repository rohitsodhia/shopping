#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"/../../../
docker compose down
docker volume rm shopping_postgres_db
./compose.sh -e dev -d

until [ "$(docker inspect -f {{.State.Running}} shopping-postgres-1)"=="true" ]; do
    sleep 0.1
done
./api/src/scripts/alembic.sh upgrade head

# until [ "$(docker inspect -f {{.State.Running}} shopping-api)"=="true" ]; do
#     sleep 0.1
# done
# docker compose exec api uv run ../scripts/populate_db.py
