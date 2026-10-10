#!/usr/bin/env python3
"""
Create a lightweight expansion-aware scaffold.

Usage:
  python scripts/scaffold_project.py --kind generic --root my-project
  python scripts/scaffold_project.py --kind web --root my-web-app
  python scripts/scaffold_project.py --kind threejs-game --root my-game
  python scripts/scaffold_project.py --kind database --root my-data-app
"""
from __future__ import annotations

import argparse
from pathlib import Path

SCAFFOLDS = {
    "generic": [
        "README.md",
        "docs/project-map.md",
        "docs/roadmap.md",
        "docs/architecture/adr/.gitkeep",
        "src/main.js",
        "src/core/.gitkeep",
        "src/config/.gitkeep",
        "src/utils/.gitkeep",
        "assets/.gitkeep",
        "tests/.gitkeep",
    ],
    "web": [
        "README.md",
        "index.html",
        "package.json",
        "docs/project-map.md",
        "src/main.js",
        "src/app/.gitkeep",
        "src/components/.gitkeep",
        "src/features/.gitkeep",
        "src/styles/tokens.css",
        "src/styles/base.css",
        "src/assets/.gitkeep",
        "src/config/.gitkeep",
        "src/utils/.gitkeep",
        "public/.gitkeep",
        "tests/.gitkeep",
    ],
    "threejs-game": [
        "README.md",
        "index.html",
        "package.json",
        "docs/project-map.md",
        "docs/roadmap.md",
        "src/main.js",
        "src/core/Game.js",
        "src/core/Renderer.js",
        "src/core/Loop.js",
        "src/core/AssetLoader.js",
        "src/scenes/MainScene.js",
        "src/entities/Player.js",
        "src/systems/InputSystem.js",
        "src/systems/CollisionSystem.js",
        "src/ui/HUD.js",
        "src/audio/AudioManager.js",
        "src/config/constants.js",
        "src/config/controls.js",
        "src/utils/math.js",
        "assets/models/.gitkeep",
        "assets/textures/.gitkeep",
        "assets/audio/.gitkeep",
        "tests/.gitkeep",
    ],
    "database": [
        "README.md",
        "docs/project-map.md",
        "db/migrations/0001_initial_schema.sql",
        "db/schema/current.sql",
        "db/seeds/dev_seed.sql",
        "db/queries/.gitkeep",
        "db/docs/erd.md",
        "db/docs/data-dictionary.md",
        "src/data/repositories/.gitkeep",
        "src/data/mappers/.gitkeep",
        "tests/.gitkeep",
    ],
}

DEFAULT_CONTENT = {
    "README.md": "# Project\n\n## Run\n\n```bash\n# TODO\n```\n\n## Structure\n\nSee `docs/project-map.md`.\n",
    "docs/project-map.md": "# Project Map\n\nDocument the current slice, north-star vision, directory map, and where future changes go.\n",
    "docs/roadmap.md": "# Roadmap\n\n## Current slice\n\n## Future expansion\n",
    "index.html": "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n  <title>Project</title>\n</head>\n<body>\n  <canvas id=\"game-canvas\"></canvas>\n  <script type=\"module\" src=\"/src/main.js\"></script>\n</body>\n</html>\n",
    "package.json": "{\n  \"scripts\": {\n    \"dev\": \"vite\",\n    \"build\": \"vite build\",\n    \"preview\": \"vite preview\"\n  },\n  \"dependencies\": {},\n  \"devDependencies\": {}\n}\n",
    "src/main.js": "// Entry point: keep thin. Initialize and hand off to project modules.\n",
    "src/core/Game.js": "export class Game {\n  start() {}\n}\n",
    "src/core/Renderer.js": "export class Renderer {}\n",
    "src/core/Loop.js": "export class Loop {}\n",
    "src/core/AssetLoader.js": "export class AssetLoader {}\n",
    "src/scenes/MainScene.js": "export class MainScene {}\n",
    "src/entities/Player.js": "export class Player {}\n",
    "src/systems/InputSystem.js": "export class InputSystem {}\n",
    "src/systems/CollisionSystem.js": "export class CollisionSystem {}\n",
    "src/ui/HUD.js": "export class HUD {}\n",
    "src/audio/AudioManager.js": "export class AudioManager {}\n",
    "src/config/constants.js": "export const GAME_CONSTANTS = {};\n",
    "src/config/controls.js": "export const CONTROLS = {};\n",
    "src/utils/math.js": "export {};\n",
    "src/styles/tokens.css": ":root {\n  /* Design tokens go here. */\n}\n",
    "src/styles/base.css": "/* Base styles go here. */\n",
    "db/migrations/0001_initial_schema.sql": "-- Initial schema migration\n",
    "db/schema/current.sql": "-- Current schema snapshot/reference\n",
    "db/seeds/dev_seed.sql": "-- Development seed data\n",
    "db/docs/erd.md": "# ERD\n\nDocument relationships here.\n",
    "db/docs/data-dictionary.md": "# Data Dictionary\n\nDocument tables and columns here.\n",
}

def create_scaffold(kind: str, root: Path) -> None:
    if kind not in SCAFFOLDS:
        raise ValueError(f"Unknown kind: {kind}")

    root.mkdir(parents=True, exist_ok=True)

    for rel in SCAFFOLDS[kind]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.name == ".gitkeep":
            path.touch(exist_ok=True)
            continue
        if path.exists():
            continue
        path.write_text(DEFAULT_CONTENT.get(rel, ""), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", required=True, choices=sorted(SCAFFOLDS))
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    create_scaffold(args.kind, Path(args.root))
    print(f"Created {args.kind} scaffold at {args.root}")

if __name__ == "__main__":
    main()
