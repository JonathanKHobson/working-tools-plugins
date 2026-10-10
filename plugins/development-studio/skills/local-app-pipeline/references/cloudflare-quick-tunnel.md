# Cloudflare Quick Tunnel

## Default policy

Use Quick Tunnel only:

```bash
cloudflared tunnel --url http://127.0.0.1:3000
```

or via the template helper:

```bash
./scripts/start-tunnel.sh
```

## Do not do by default

- Do not run `cloudflared tunnel login`
- Do not create named tunnels
- Do not create hostname routes
- Do not create `~/.cloudflared/config.yml`

## Why

This account has no Cloudflare zone/domain available, so named tunnels do not provide value for this workflow.

## Failure handling

If Quick Tunnel returns a Cloudflare-hosted error page such as a `1101` from `api.trycloudflare.com`, treat it as a Cloudflare-side availability problem unless the local app itself is down.
