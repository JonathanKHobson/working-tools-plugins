---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first, fetch review threads, classify comments by severity and actionability, apply systematic debugging for bug comments, and verify fixes before reporting.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` (include workflow/repo scopes when needed). If the current environment blocks network auth checks, report that plainly instead of pretending review comments were inspected.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Classify each comment:
  - `bug/security/data-loss`: root-cause with `$systematic-debugging` before editing
  - `test gap`: add or update a meaningful regression test where the repo has a seam
  - `style/mechanical`: safe to patch directly
  - `ambiguous/product`: ask the user before changing behavior
  - `external/unactionable`: report, do not invent work
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments
- Verify each fix with the nearest test, build, lint, or manual reproduction.
- If a comment points to a branch or trust-boundary risk, review adjacent code outside the diff before claiming it is resolved.

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
