# Codex Local App Template Instructions

Use this project as a local-first app template.

## Defaults
- Run the preview app on port `3000`.
- Run PocketBase on port `8090`.
- Use `./scripts/start-dev.sh` to start local services.
- Use `./scripts/start-tunnel.sh` to share the app.
- Prefer Docker named volumes for persistent app data.
- Keep Quick Tunnel as the default public preview workflow.

## When adding a real app
- Keep the preview reachable at `http://127.0.0.1:3000`.
- If needed, set `APP_START_CMD` in `.env`.
- Prefer PocketBase for auth, shared records, and file storage unless the user asks for another backend.
- Avoid creating `~/.cloudflared/config.yml` when Quick Tunnel is the goal.

## Expected commands
- `./scripts/check-ports.sh`
- `./scripts/start-dev.sh`
- `./scripts/start-tunnel.sh`
