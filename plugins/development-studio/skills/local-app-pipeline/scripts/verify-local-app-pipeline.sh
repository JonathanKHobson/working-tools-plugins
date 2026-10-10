#!/usr/bin/env bash
set -euo pipefail

: "${LOCAL_APP_PIPELINE_ROOT:?Set the external pipeline workspace}"
: "${LOCAL_APP_PIPELINE_DOCKER_STORAGE:?Set reviewed external Docker storage}"
WORKSPACE="${LOCAL_APP_PIPELINE_ROOT}"
TEMPLATE="$WORKSPACE/template"
DOCKER_EXTERNAL="${LOCAL_APP_PIPELINE_DOCKER_STORAGE}"
DOCKER_INTERNAL="$HOME/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw"
SKILL_LINK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  echo "FAIL: $1"
  exit 1
}

warn() {
  echo "WARN: $1"
}

pass() {
  echo "PASS: $1"
}

command -v docker >/dev/null 2>&1 || fail "docker is not installed or not on PATH"
command -v cloudflared >/dev/null 2>&1 || fail "cloudflared is not installed or not on PATH"

[[ -d "$WORKSPACE" ]] || fail "workspace missing"
[[ -d "$TEMPLATE" ]] || fail "template missing"
[[ -f "$TEMPLATE/scripts/start-dev.sh" ]] || fail "start-dev.sh missing"
[[ -f "$TEMPLATE/scripts/start-tunnel.sh" ]] || fail "start-tunnel.sh missing"
[[ -f "$TEMPLATE/scripts/check-ports.sh" ]] || fail "check-ports.sh missing"
[[ -L "$SKILL_LINK" || -d "$SKILL_LINK" ]] || fail "installed skill missing from ~/.codex/skills"

docker info >/dev/null 2>&1 || fail "docker daemon is not healthy"
pass "docker daemon is healthy"

if [[ -f "$DOCKER_INTERNAL" ]]; then
  warn "internal Docker.raw still exists at $DOCKER_INTERNAL"
fi

if [[ -d "$DOCKER_EXTERNAL" ]]; then
  if find "$DOCKER_EXTERNAL" -mindepth 1 -maxdepth 2 | read -r _; then
    pass "external DockerDesktop target has content"
  else
    warn "external DockerDesktop target is still empty"
  fi
else
  fail "external DockerDesktop target missing"
fi

if [[ -f "$HOME/.cloudflared/config.yml" ]]; then
  warn "~/.cloudflared/config.yml exists and may block Quick Tunnel"
else
  pass "Quick Tunnel config precondition is clean"
fi

pass "local app pipeline verification completed"
