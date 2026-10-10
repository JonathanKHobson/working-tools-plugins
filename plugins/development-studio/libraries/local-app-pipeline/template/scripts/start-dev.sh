#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"
EXAMPLE_ENV_FILE="$ROOT_DIR/.env.example"
PUBLIC_DIR="$ROOT_DIR/public"

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$EXAMPLE_ENV_FILE" "$ENV_FILE"
fi

set -a
source "$ENV_FILE"
set +a

APP_PORT="${APP_PORT:-3000}"
APP_HOST="${APP_HOST:-127.0.0.1}"
POCKETBASE_PORT="${POCKETBASE_PORT:-8090}"
APP_START_CMD="${APP_START_CMD:-}"

export APP_PORT
export PORT="$APP_PORT"
export HOST="$APP_HOST"
export POCKETBASE_PORT

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1"
    exit 1
  fi
}

wait_for_docker() {
  local attempts=60
  until docker info >/dev/null 2>&1; do
    ((attempts--))
    if (( attempts == 0 )); then
      echo "Docker Desktop is not ready."
      exit 1
    fi
    sleep 2
  done
}

wait_for_port() {
  local port="$1"
  local attempts=30
  until lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; do
    ((attempts--))
    if (( attempts == 0 )); then
      return 1
    fi
    sleep 1
  done
}

cleanup() {
  if [[ -n "${APP_PID:-}" ]] && kill -0 "$APP_PID" >/dev/null 2>&1; then
    kill "$APP_PID" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

require_cmd docker
require_cmd python3

if ! docker info >/dev/null 2>&1; then
  open -a Docker
fi

wait_for_docker

docker compose -f "$ROOT_DIR/docker-compose.yml" up -d pocketbase

if ! wait_for_port "$POCKETBASE_PORT"; then
  echo "PocketBase did not open on port $POCKETBASE_PORT."
  exit 1
fi

echo "PocketBase is running at http://127.0.0.1:$POCKETBASE_PORT"
echo "PocketBase admin UI: http://127.0.0.1:$POCKETBASE_PORT/_/"

if [[ -z "$APP_START_CMD" ]]; then
  echo "APP_START_CMD is empty. Serving $PUBLIC_DIR on port $APP_PORT."
  python3 -m http.server "$APP_PORT" --bind "$APP_HOST" --directory "$PUBLIC_DIR" &
  APP_PID=$!
else
  echo "Starting app command: $APP_START_CMD"
  bash -lc "$APP_START_CMD" &
  APP_PID=$!
fi

if ! wait_for_port "$APP_PORT"; then
  echo "App preview did not open on port $APP_PORT."
  exit 1
fi

echo "Local app preview: http://$APP_HOST:$APP_PORT"
wait "$APP_PID"
