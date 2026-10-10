#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"
EXAMPLE_ENV_FILE="$ROOT_DIR/.env.example"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$EXAMPLE_ENV_FILE" "$ENV_FILE"
fi

set -a
source "$ENV_FILE"
set +a

APP_PORT="${APP_PORT:-3000}"
POCKETBASE_PORT="${POCKETBASE_PORT:-8090}"

show_port() {
  local port="$1"
  echo "== Port $port =="
  if lsof -nP -iTCP:"$port" -sTCP:LISTEN; then
    :
  else
    echo "free"
  fi
  echo
}

show_port "$APP_PORT"
show_port "$POCKETBASE_PORT"
