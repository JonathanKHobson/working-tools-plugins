# Local App Pipeline Workspace

This workspace is the single source of truth for the local-first app pipeline on the receiving host.

## What is installed

- Docker Desktop in `/Applications/Docker.app`
- `cloudflared` via Homebrew
- A reusable starter template in `./template`
- A reusable Codex skill in `./skill/local-app-pipeline`

## Current status

The local setup is complete.

What is working:

- Docker Desktop is healthy
- Docker storage is on the external SSD
- the starter template is reusable
- the installed Codex skill points at this workspace
- PocketBase runs on `8090`
- app previews run on `3000`

Verify current receiving-host status with the included check script; this export asserts no live provider state.

## How the pipeline works

### Local app workflow

- Run the app preview on `127.0.0.1:3000`
- Run PocketBase on `127.0.0.1:8090`
- Use Docker named volumes for shared data
- Use Cloudflare Quick Tunnel only when you want a temporary public preview

### Why this setup exists

This workflow avoids paid hosting and domains while still letting apps:

- have auth
- store shared data
- expose a temporary preview URL
- stay mostly local-first

## Canonical paths

- Workspace root:
  `${LOCAL_APP_PIPELINE_ROOT}`
- Starter template:
  `${LOCAL_APP_PIPELINE_ROOT}/template`
- Skill source:
  `${LOCAL_APP_PIPELINE_ROOT}/skill/local-app-pipeline`
- Installed skill link:
  `${DEVELOPMENT_STUDIO_ROOT}/skills/local-app-pipeline`

## How to use this from now on

Read [references/how-to-use-this.md](./references/how-to-use-this.md).

That walkthrough is the standard operating flow for:

- starting a new app from this pipeline
- wiring a real app into port `3000`
- using PocketBase for auth and shared data
- using Quick Tunnel for temporary previews
- invoking `$local-app-pipeline` in future Codex work

## Start the stack

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/start-dev.sh
```

That starts:

- PocketBase on `8090`
- the fallback preview app or your real app on `3000`

## Share the app

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/start-tunnel.sh
```

Quick Tunnel is the default sharing workflow because:

- it does not require a domain
- it does not require `cloudflared tunnel login`
- it fits the temporary-preview use case

Quick Tunnel is still subject to Cloudflare service availability. A prior test reached Cloudflare successfully but failed with a Cloudflare-side `1101` error from `api.trycloudflare.com`.
That retest was reproduced again after the workspace and skill were finalized, so this is currently documented as an external-service issue rather than a local setup issue.

## Why named tunnels are skipped

Named tunnels are not part of this setup because there is no existing Cloudflare zone/domain in the account. Without a zone, `cloudflared tunnel login` cannot complete in a useful way for a persistent hostname workflow.

## Layout

- `README.md`
  Primary operator guide
- `status.md`
  Live completion status
- `references/how-to-use-this.md`
  End-to-end future-use walkthrough
- `references/commands.md`
  Copy-paste commands
- `references/troubleshooting.md`
  Known issues and recovery steps
- `template/`
  Reusable starter project
- `skill/local-app-pipeline/`
  Source-of-truth Codex skill

## Housekeeping

This workspace ignores Finder metadata noise where possible. Avoid copying AppleDouble `._*` files into the workspace. A `.gitignore` is included to document that convention.
