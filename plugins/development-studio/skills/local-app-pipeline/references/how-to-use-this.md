# How To Use This Skill

Use this reference as the default operating flow for future projects that rely on the local app pipeline.

## What this skill is for

This skill exists to keep Codex aligned with the established local-first workflow on the receiving host.

That means:

- reuse the pipeline workspace
- prefer the existing template
- keep app previews on port `3000`
- keep PocketBase on `8090`
- use Quick Tunnel only for temporary sharing

## Default future-project flow

### 1. Start from the canonical workspace

Canonical workspace:

`${LOCAL_APP_PIPELINE_ROOT}`

Canonical template:

`${LOCAL_APP_PIPELINE_ROOT}/template`

Do not invent a parallel local infra stack unless the user explicitly asks for a different architecture.

### 2. Keep the standard contract

- app preview on `127.0.0.1:3000`
- PocketBase on `127.0.0.1:8090`
- Docker named volumes for persistent backend data

### 3. Wire the real app through `APP_START_CMD` when needed

If the project has a real app server, set `APP_START_CMD` in `.env` so `start-dev.sh` still controls the whole workflow.

### 4. Use the template scripts

- `./scripts/check-ports.sh`
- `./scripts/start-dev.sh`
- `./scripts/start-tunnel.sh`

### 5. Use Cloudflare correctly

- Use Quick Tunnel only.
- Do not require a domain.
- Do not use named tunnels unless the user explicitly changes scope and has a real Cloudflare zone.

## What to tell the user

When helping with future projects, explain that they can explicitly invoke:

`$local-app-pipeline`

and Codex should reuse this workspace and workflow rather than creating a fresh setup.

## Known caveat

Quick Tunnel can still fail because of Cloudflare-side `1101` errors from `api.trycloudflare.com` even when the local setup is correct. Treat that as an upstream dependency issue first.
