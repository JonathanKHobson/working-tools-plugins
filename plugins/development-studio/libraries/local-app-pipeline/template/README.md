# Codex Local App Template

This template gives you a local-first app workflow with:

- Docker Desktop for containers
- PocketBase for auth, data, and file storage
- Cloudflare Quick Tunnel for easy preview sharing
- A default preview target on `http://127.0.0.1:3000`

## What this template does

- Starts PocketBase in Docker on port `8090`
- Starts a preview app on port `3000`
- Lets you share the preview with one command using a Cloudflare Quick Tunnel
- Keeps PocketBase data in a Docker named volume instead of local project files

## Prerequisites

- Docker Desktop installed and running
- `cloudflared` installed
- No `~/.cloudflared/config.yml` file if you want Quick Tunnel to work

## First run

1. Copy this template into a new project folder.
2. In the new project folder, copy `.env.example` to `.env` if you want to customize ports or startup behavior.
3. Run:

```bash
./scripts/start-dev.sh
```

If you have not set `APP_START_CMD`, the script serves the `public/` folder as a placeholder app on port `3000`.

## Share the app

With the local app running on port `3000`, run:

```bash
./scripts/start-tunnel.sh
```

That prints a temporary `trycloudflare.com` URL you can share.

## PocketBase

- PocketBase URL: `http://127.0.0.1:8090`
- PocketBase admin UI: `http://127.0.0.1:8090/_/`

Create your first PocketBase superuser with:

```bash
docker compose exec pocketbase /pocketbase/pocketbase superuser create you@example.com your-password
```

After that, use PocketBase collections for:

- email/password auth
- OAuth providers
- record storage
- file uploads

## Customizing the app command

Set `APP_START_CMD` in `.env` to your real app startup command. Examples:

```bash
APP_START_CMD=npm run dev -- --host 127.0.0.1 --port 3000
```

```bash
APP_START_CMD=python3 -m http.server 3000 --bind 127.0.0.1
```

The scripts export `APP_PORT`, `PORT`, and `HOST` before starting your app.

## Helpful commands

```bash
./scripts/check-ports.sh
```

```bash
docker compose logs -f pocketbase
```

```bash
docker compose down
```

## Storage and space

- PocketBase persists in a Docker named volume.
- Docker Desktop should keep its disk image on the external SSD at:
  `${LOCAL_APP_PIPELINE_DOCKER_STORAGE}`
- Homebrew cache has been moved to the external SSD via symlink.

## Recommended future workflow

1. Build your app so it serves on port `3000`.
2. Use PocketBase on port `8090` for auth and shared data.
3. Use `./scripts/start-tunnel.sh` whenever you want to preview it remotely.
