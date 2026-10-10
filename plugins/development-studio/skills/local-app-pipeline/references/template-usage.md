# Template Usage

## Template root

`${LOCAL_APP_PIPELINE_ROOT}/template`

## Read this first

Use `references/how-to-use-this.md` for the full operating walkthrough. Use this file for template-specific details only.

## Standard commands

- `./scripts/check-ports.sh`
- `./scripts/start-dev.sh`
- `./scripts/start-tunnel.sh`

## Integration guidance

- Keep the real app reachable on port `3000`.
- Set `APP_START_CMD` in `.env` when replacing the fallback static server.
- Keep PocketBase running on `8090`.
- Prefer PocketBase for auth, shared records, and uploads unless the user explicitly wants another backend.

## Clean template behavior

The template should rely on `.env.example` and generate `.env` locally when needed. It should not ship with a committed `.env` file as the source template.
