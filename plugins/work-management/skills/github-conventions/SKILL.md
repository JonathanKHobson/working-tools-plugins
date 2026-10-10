---
name: github-conventions
description: Use when working with the configured GitHub account, repos, branches, or uploads; when an agent needs account orientation, needs to push a local project to GitHub safely, needs to decide whether to use a repo root or a subfolder, needs to refresh a repo/branch/file map using gh, or needs GitHub navigation shortcuts, commit permalinks, version comparisons, source snapshots, or reviewed repository context tools.
---

# GitHub Account Conventions

## Overview

This skill captures the working conventions for the configured GitHub account
so agents can upload projects safely, use the right repo, avoid
clobbering existing content, and explain Git terms in plain language when the
user is not Git-native.

Account default:

- GitHub owner: `${GITHUB_OWNER}`
- Preferred CLI: `gh`
- Preferred git transport after login: `https`

## Workflow

1. Confirm auth when account access or a write requires it.
   Run `gh auth status`. If needed, use `gh auth login --web`. Public
   read-only browsing does not require initiating a login.
2. Inspect the destination repo before copying files.
   Check default branch, current top-level contents, and whether the repo root
   already contains unrelated work.
3. Prefer the safest placement when user intent is ambiguous.
   If the repo already has content and the user asks to "upload this project,"
   prefer a new top-level folder instead of replacing the repo root.
4. Explain branches in plain language when needed.
   Treat a branch as a separate version lane. If the user does not intentionally
   use branches, default to the repo's default branch after confirming the repo.
5. Avoid destructive pushes.
   Do not remove unrelated files from an existing repo unless the user clearly
   asks to replace them.
6. Refresh the account map when repo state matters.
   Run `scripts/refresh_account_map.py` to regenerate the live inventory in
   `references/account-map.md`.
7. Before publishing public artifacts, run a sink review.
   Check the outgoing files, PR body, commit message, and README for secrets,
   private paths, accidental local-only instructions, and stale claims. Public
   shareables should link to source repos and evidence without exposing local
   credentials, browser sessions, or private project paths unless intentional.
8. For non-trivial code pushes, use the local ship gate:
   tests/build where available, `$systematic-debugging` for failures,
   review findings first, then push/PR. Do not treat "git status is clean" as
   evidence that the change works.

For repository browsing, stable evidence links, browser edits, or optional AI
repository helpers, load `references/repository-navigation.md` only when relevant.
Its source and privacy checks also apply when gathering context for an upload.

## Trigger Examples

- "Upload this project to my GitHub."
- "Which repo should this go in on my GitHub?"
- "Map my repos and branches."
- "I don't know what a branch is."
- "Push this to the configured GitHub account."
- "Can you see all the files in my GitHub?"
- "Give me a stable link to these lines or compare these versions."
- "Show me faster ways to inspect this GitHub repo."
- "Would GitDiagram, Gitingest, DeepWiki, or GitMCP help here?"

## Reference Map

- For shortcuts, permalinks, comparisons, downloads, and reviewed context options:
  `references/repository-navigation.md`

- For the live repo, branch, and file inventory:
  `references/account-map.md`
- To refresh that inventory from GitHub:
  `scripts/refresh_account_map.py`

## Rules

- Use `gh` for account discovery and authentication.
- Prefer `gh repo list ${GITHUB_OWNER} ...` over guessing repo names.
- Before pushing, inspect the target repo contents and branch list.
- If a repo root already contains unrelated projects, upload new work into a
  dedicated top-level folder unless the user explicitly wants replacement.
- Exclude junk files like `._*`, `.DS_Store`, local env files, and dependency
  folders unless the repo intentionally tracks them.
- Exclude secrets, `.env*`, browser profiles, cookies, private logs, MCP tokens,
  and generated security reports that include local-only details.
- When the user is unfamiliar with GitHub, explain only the minimum needed to
  choose a safe action.
