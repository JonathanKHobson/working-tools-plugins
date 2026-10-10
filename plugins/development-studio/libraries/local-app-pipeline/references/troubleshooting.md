# Troubleshooting

## Docker still using internal storage

Symptom:

- `~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw` is still the active disk image
- `${LOCAL_APP_PIPELINE_DOCKER_STORAGE}` is empty

Fix:

1. Open Docker Desktop.
2. Go to:
   `Settings > Resources > Advanced`
3. Change:
   `Disk image location`
4. Select:
   `${LOCAL_APP_PIPELINE_DOCKER_STORAGE}`
5. Click:
   `Apply & Restart`

Re-check after restart:

- Docker still starts normally
- external Docker folder is populated
- internal `Docker.raw` is no longer the active disk location

## Cloudflare Quick Tunnel fails

Quick Tunnel can fail even when the local machine is configured correctly.

Known observed case:

- Cloudflare returned a `1101` error from `api.trycloudflare.com`
- The same `1101` failure was reproduced on a later retest after the workspace and skill were finalized

Interpretation:

- local `cloudflared` was installed and launched correctly
- the failure was upstream on Cloudflare's side

What to do:

1. Confirm the local app is listening on `3000`
2. Retry `./scripts/start-tunnel.sh`
3. If it still fails with a Cloudflare-side error page, treat it as an external availability issue

## `~/.cloudflared/config.yml` blocks Quick Tunnel

Quick Tunnel should be run without a persistent `cloudflared` config file in `~/.cloudflared/config.yml`.

If that file exists, remove or rename it before using this workflow.

## No Cloudflare zone available

If the Cloudflare account has no existing zone/domain:

- do not use `cloudflared tunnel login`
- do not create named tunnels
- do not create hostname routes

Use Quick Tunnel only.

## Finder metadata clutter on the external SSD

If you see `._*` files inside the pipeline workspace, they are Finder metadata sidecars.

Safe cleanup for this workspace only:

```bash
find '${LOCAL_APP_PIPELINE_ROOT}' -name '._*' -delete
```

## Port conflicts

Check ports:

```bash
cd '${LOCAL_APP_PIPELINE_ROOT}/template' && ./scripts/check-ports.sh
```

Expected defaults:

- app preview: `3000`
- PocketBase: `8090`
