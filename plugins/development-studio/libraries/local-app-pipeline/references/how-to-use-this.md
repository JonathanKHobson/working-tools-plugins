# How To Use This From Now On

## What this is

This workspace gives you a reusable local-first app pipeline on the receiving host.

It includes:

- a starter template in `template/`
- PocketBase for auth, shared records, and uploads
- Cloudflare Quick Tunnel for temporary public previews
- an installed Codex skill called `$local-app-pipeline`

Use it whenever you want to build or test an app without paying for hosting or buying a domain.

## Where everything lives

- Workspace:
  `${LOCAL_APP_PIPELINE_ROOT}`
- Template:
  `${LOCAL_APP_PIPELINE_ROOT}/template`
- Installed skill:
  `${DEVELOPMENT_STUDIO_ROOT}/skills/local-app-pipeline`

## Typical future project flow

### 1. Start from the template

If you are starting a new project, copy or adapt the template in `template/`.

The template already assumes:

- app preview on `127.0.0.1:3000`
- PocketBase on `127.0.0.1:8090`
- Docker named volumes for persistent backend data

### 2. Point your real app at port 3000

If your real app needs a custom startup command, set `APP_START_CMD` in `.env`.

Example:

```bash
APP_START_CMD=npm run dev -- --host 127.0.0.1 --port 3000
```

The contract is simple:

- your app must be reachable on port `3000`
- PocketBase stays on `8090`

### 3. Start the stack

Use:

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/start-dev.sh
```

That starts:

- PocketBase on `8090`
- the fallback static app or your real app on `3000`

### 4. Confirm everything is live

Check:

- app preview at `http://127.0.0.1:3000`
- PocketBase admin at `http://127.0.0.1:8090/_/`

You can also run the stable helper commands listed in [commands.md](./commands.md).

### 5. Share a temporary public preview

When you want to share the app:

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/start-tunnel.sh
```

This uses Cloudflare Quick Tunnel only.

## How to use PocketBase

Use PocketBase when the app needs:

- user accounts
- shared records
- file uploads
- non-local-only data

Default address:

- `http://127.0.0.1:8090`

Create the first superuser with the command listed in [commands.md](./commands.md).

## How to use this with Codex

In future projects, explicitly reference the installed skill:

```text
Use $local-app-pipeline for this app.
```

That should signal Codex to:

- reuse this workspace instead of inventing a new stack
- keep the app on port `3000`
- keep PocketBase on `8090`
- use Quick Tunnel for previews
- avoid domains, paid hosting, and named Cloudflare tunnels unless you explicitly ask for them

## Known caveats

- Quick Tunnel may fail even when your local setup is correct.
- The observed failure here is a Cloudflare-side `1101` from `api.trycloudflare.com`.
- If that happens, treat it as an external service issue first, not a local misconfiguration.

## Stable commands

Do not memorize every command from chat history.

Use:

- [commands.md](./commands.md)

That file is the stable copy-paste command list for this workspace.
