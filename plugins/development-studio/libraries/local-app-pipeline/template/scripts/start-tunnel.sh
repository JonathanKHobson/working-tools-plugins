#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"
EXAMPLE_ENV_FILE="$ROOT_DIR/.env.example"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared is not installed."
  exit 1
fi

if [[ -f "$HOME/.cloudflared/config.yml" ]]; then
  echo "~/.cloudflared/config.yml exists. Quick Tunnel requires that file to be absent."
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$EXAMPLE_ENV_FILE" "$ENV_FILE"
fi

set -a
source "$ENV_FILE"
set +a

APP_PORT="${APP_PORT:-3000}"
APP_HOST="${APP_HOST:-127.0.0.1}"

if ! lsof -nP -iTCP:"$APP_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Nothing is listening on port $APP_PORT."
  echo "Start the app first with ./scripts/start-dev.sh"
  exit 1
fi

echo "Starting Cloudflare Quick Tunnel for http://$APP_HOST:$APP_PORT"
exec cloudflared tunnel --url "http://$APP_HOST:$APP_PORT"
