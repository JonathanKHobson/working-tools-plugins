#!/usr/bin/env python3

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


OWNER = None
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = None


def run_json(*args):
    result = subprocess.run(
        args,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def repo_list():
    return run_json(
        "gh",
        "repo",
        "list",
        OWNER,
        "--limit",
        "200",
        "--json",
        ",".join(
            [
                "name",
                "nameWithOwner",
                "description",
                "isPrivate",
                "isFork",
                "defaultBranchRef",
                "url",
                "primaryLanguage",
                "pushedAt",
            ]
        ),
    )


def repo_branches(repo_name):
    return run_json(
        "gh",
        "api",
        f"repos/{OWNER}/{repo_name}/branches",
        "--paginate",
    )


def repo_tree(repo_name, branch_name):
    branch_data = run_json(
        "gh",
        "api",
        f"repos/{OWNER}/{repo_name}/branches/{branch_name}",
    )
    tree_sha = branch_data["commit"]["commit"]["tree"]["sha"]
    data = run_json(
        "gh",
        "api",
        f"repos/{OWNER}/{repo_name}/git/trees/{tree_sha}?recursive=1",
    )
    return data.get("tree", [])


def top_level_entries(tree_items):
    names = {}
    for item in tree_items:
        path = item.get("path", "")
        if "/" in path or not path:
            continue
        names[path] = item.get("type", "unknown")
    return [{"name": name, "type": names[name]} for name in sorted(names)]


def format_repo_section(repo):
    repo_name = repo["name"]
    default_branch = repo["defaultBranchRef"]["name"]
    branches = sorted(branch["name"] for branch in repo_branches(repo_name))
    tree_items = repo_tree(repo_name, default_branch)
    files = sorted(
        item["path"] for item in tree_items if item.get("type") == "blob" and item.get("path")
    )
    dirs = sorted(
        item["path"] for item in tree_items if item.get("type") == "tree" and item.get("path")
    )
    top_level = top_level_entries(tree_items)
    language = repo["primaryLanguage"]["name"] if repo.get("primaryLanguage") else "Unknown"
    description = repo.get("description") or "No description"
    visibility = "private" if repo.get("isPrivate") else "public"
    fork_flag = "fork" if repo.get("isFork") else "source"
    top_level_text = (
        ", ".join(f"`{entry['name']}` ({entry['type']})" for entry in top_level)
        if top_level
        else "None"
    )

    lines = [
        f"## {repo['nameWithOwner']}",
        "",
        f"- URL: {repo['url']}",
        f"- Default branch: `{default_branch}`",
        f"- Branches: {', '.join(f'`{branch}`' for branch in branches)}",
        f"- Visibility: {visibility}",
        f"- Type: {fork_flag}",
        f"- Primary language: {language}",
        f"- Last pushed: {repo['pushedAt']}",
        f"- Description: {description}",
        f"- Top-level entries: {top_level_text}",
        f"- Directory count on `{default_branch}`: {len(dirs)}",
        f"- File count on `{default_branch}`: {len(files)}",
        "",
        "### Full file tree",
        "",
    ]

    if files:
        lines.extend(f"- `{path}`" for path in files)
    else:
        lines.append("- No files found")

    return "\n".join(lines)


def main(argv=None):
    global OWNER, OUTPUT
    parser = argparse.ArgumentParser(description="Refresh an explicitly selected recipient GitHub account map.")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--output", required=True, type=Path)
    options = parser.parse_args(argv)
    OWNER, OUTPUT = options.owner, options.output.expanduser().resolve()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    repos = sorted(repo_list(), key=lambda item: item["name"].lower())
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    lines = [
        f"# {OWNER} GitHub Map",
        "",
        f"Generated from live GitHub data via `gh` on {generated_at}.",
        "",
        "## Summary",
        "",
        f"- Repo count: {len(repos)}",
    ]

    if repos:
        defaults = sorted({repo["defaultBranchRef"]["name"] for repo in repos})
        repo_names = ", ".join(f"`{repo['name']}`" for repo in repos)
        lines.append(
            f"- Default branches seen: {', '.join(f'`{name}`' for name in defaults)}"
        )
        lines.append(f"- Repo names: {repo_names}")

    lines.append("")

    for repo in repos:
        lines.append(format_repo_section(repo))
        lines.append("")

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
