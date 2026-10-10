---
name: local-app-pipeline
description: Reuse and maintain the local-first app pipeline on the receiving host using Docker Desktop, PocketBase, and Cloudflare Quick Tunnel. Use when Codex needs to set up or extend a web app, local backend, preview environment, or app-sharing workflow that should stay free, local-first, and external-SSD-aware; when a project needs auth, shared records, or file storage via PocketBase; when a project must serve on port 3000 and share previews with Quick Tunnel; or when Codex must verify Docker storage location, template usage, or the pipeline workspace under ${LOCAL_APP_PIPELINE_ROOT}.
---

# Local App Pipeline

Use the existing authorized recipient pipeline before inventing a new local app setup. The complete original Docker/PocketBase/Quick Tunnel method, verification script and reusable template are included. Set LOCAL_APP_PIPELINE_ROOT to an external workspace and LOCAL_APP_PIPELINE_DOCKER_STORAGE to the reviewed receiving-host storage location. Copy the template into that workspace before invoking launch scripts. Docker Desktop, a reviewed/pinned PocketBase image, cloudflared, accounts, storage and network-sharing authorization are external requirements; no service or tunnel is started by installation.

## Coordination and MCP Awareness

- Start with this skill when the task is a local-first web app, Docker/PocketBase setup, preview pipeline, or Quick Tunnel workflow on the receiving host.
- Use `mac-environment-conventions` when drive choice, app/runtime placement, or external-storage rules materially affect the setup.
- Use `storage-memory-manager` when Docker storage, cache growth, or disk pressure becomes part of the problem.
- Use `chatgpt-apps` when the local app is specifically a ChatGPT Apps SDK app with an MCP server and widget UI.
- Use `local-data-mcp-builder` when the app needs a local indexed data MCP rather than only app infrastructure.
- Use `local-mcp-debugging` when a local MCP in the pipeline will not attach or survive startup.
- Use `playwright` when browser-level validation is the fastest way to confirm the preview flow works.

## Quick Start

1. Check whether the canonical workspace already exists at `${LOCAL_APP_PIPELINE_ROOT}`.
2. Reuse the complete template in `../../libraries/local-app-pipeline/template/` unless the user explicitly wants a different stack.
3. Keep the app preview on `127.0.0.1:3000`.
4. Keep PocketBase on `127.0.0.1:8090`.
5. Use Cloudflare Quick Tunnel only. Do not ask for a domain or configure named tunnels by default.
6. Read `references/how-to-use-this.md` for the standard operating flow before improvising.

## Workflow

### 1. Verify the machine state

- Confirm Docker Desktop is installed and running.
- Confirm `cloudflared` is installed.
- Check whether Docker still uses the internal `Docker.raw`.
- If Docker is still on internal storage, call it out clearly and point to `references/docker-storage.md`.

### 2. Reuse the existing template

- Start from `${LOCAL_APP_PIPELINE_ROOT}/template`.
- Prefer adapting that template over creating a new local infra stack.
- Read `references/how-to-use-this.md` first, then `references/template-usage.md` when wiring a new project into the pipeline.

### 3. Enforce the contract

- Preview app must listen on port `3000`.
- PocketBase must stay on `8090`.
- Shared app data should use Docker named volumes.
- Avoid paid hosting and domain requirements unless the user explicitly changes direction.

### 4. Use Cloudflare correctly

- Use Quick Tunnel only.
- Do not run `cloudflared tunnel login` unless the user later adds a real Cloudflare zone and explicitly wants persistent hostnames.
- Do not create `~/.cloudflared/config.yml` for this workflow.
- If Quick Tunnel fails with a Cloudflare-side error, treat it as external service instability and document it rather than misdiagnosing the local machine.

### 5. Verify after changes

- Use `scripts/verify-local-app-pipeline.sh` for a deterministic local check.
- Re-run the template scripts if the project wiring changed.

## References

- `references/current-workflow.md`
  Read for the canonical workspace layout and project conventions.
- `references/how-to-use-this.md`
  Read for the standard future-use walkthrough and expected operating flow.
- `references/docker-storage.md`
  Read when Docker storage location or disk pressure matters.
- `references/cloudflare-quick-tunnel.md`
  Read when preview sharing or Cloudflare behavior is relevant.
- `references/template-usage.md`
  Read when integrating a real project into the template.

## Non-Negotiable Defaults

- Prefer the existing workspace instead of inventing a fresh stack.
- Keep preview apps on port `3000`.
- Keep PocketBase on port `8090`.
- Use Docker named volumes for persistent app data.
- Do not ask the user to buy a domain.
- Use Quick Tunnel as the default preview-sharing method.
- If the Docker disk image has not been moved to the external SSD yet, call that out before declaring the setup complete.

## Project organization guardrail

Before creating or expanding web/app project files, consult the `work-management:project-structure` skill. If the user explicitly requests a self-contained one-file HTML deliverable, single-file output is allowed; otherwise, expandable websites and apps should separate HTML, CSS, JavaScript/TypeScript, assets, components/features, docs, and tests according to framework conventions.

When the user provides a north-star vision, roadmap, multi-phase goal, or future expansion hints, create a lightweight expansion-aware folder/file plan before implementation.
