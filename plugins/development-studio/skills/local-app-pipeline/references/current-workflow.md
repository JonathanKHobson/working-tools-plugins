# Current Workflow

## Canonical workspace

- Workspace root:
  `${LOCAL_APP_PIPELINE_ROOT}`
- Starter template:
  `${LOCAL_APP_PIPELINE_ROOT}/template`
- Installed skill link:
  `${DEVELOPMENT_STUDIO_ROOT}/skills/local-app-pipeline`

## Default behavior

- App preview on `127.0.0.1:3000`
- PocketBase on `127.0.0.1:8090`
- Shared data via Docker named volumes
- Quick Tunnel only for public previews

## Key decisions

- No domain purchase
- No named tunnels
- No persistent Cloudflare hostname
- Local-first workflow optimized for experimentation

## Reuse rule

If a future project needs auth, shared records, file storage, or preview sharing, start from the existing template and adapt it rather than scaffolding a new stack from scratch.

## Operator walkthrough

For the standard future-use flow, read `references/how-to-use-this.md`.
