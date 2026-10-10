---
name: "develop-web-game"
description: "Use when Codex is building or iterating on a web game (HTML/JS) and needs a reliable development + testing loop: implement small changes, coordinate with game-design, frontend UX, UX writing, communication, or Game Studio guidance when it materially changes the build, run a Playwright-based test script with short input bursts and intentional pauses, inspect screenshots/text, and review console errors with render_game_to_text."
---


# Develop Web Game

Build games in small steps and validate every change. Treat each iteration as: implement → act → pause → observe → adjust.

## Skill paths (set once)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEB_GAME_CLIENT="$CODEX_HOME/skills/develop-web-game/scripts/web_game_playwright_client.js"
export WEB_GAME_ACTIONS="$CODEX_HOME/skills/develop-web-game/references/action_payloads.json"
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

## Related Skills and Routing

This skill owns the build-and-test loop for playable browser games. Keep it as the center of gravity once implementation starts, and load adjacent skills only when they change the next concrete build decision.

- Use `$game-designer` before or alongside this skill when the game fantasy, player verbs, core loop, balance, progression, encounter design, onboarding pace, or playtest hypothesis is unclear. Return with the smallest buildable design artifact: a mechanic spec, loop sheet, balance note, or playtest plan.
- Use `$frontend-ux` when HUDs, menus, overlays, responsive behavior, accessibility, state coverage, input feedback, or visible UI behavior affects playability. Treat missing focus states, unclear hierarchy, broken mobile layout, and unreadable state as implementation bugs.
- Use `$ux-writer` when the game needs user-facing text decisions: control labels, tutorial hints, button copy, error/recovery messages, empty states, tooltips, menu labels, onboarding copy, or confirmation text. Keep game UI copy short, specific, and timed to the moment of need.
- Use `$communication-story-crafter` when the output needs a player-facing premise, devlog, stakeholder update, portfolio framing, pitch, teaching explanation, or public proof narrative. Do not let story framing delay the playable build unless the user asked for the communication artifact.
- Use the Game Studio plugin under `$CODEX_HOME/plugins/cache/openai-curated/game-studio` when the task needs engine routing, shared browser-game architecture, Phaser/Three.js/React Three Fiber execution guidance, sprite or 3D asset pipeline help, game UI frontend patterns, or structured playtest review. Its skills live inside the plugin's versioned `skills/` directory. Prefer the most specific Game Studio skill once the route is clear: `game-studio`, `web-game-foundations`, `phaser-2d-game`, `three-webgl-game`, `react-three-fiber-game`, `sprite-pipeline`, `web-3d-asset-pipeline`, `game-ui-frontend`, or `game-playtest`.

Default routing rule: if the user asked to build or fix a playable web game, do not stay in planning. Take the smallest useful pass through the relevant adjacent skill, then implement and verify in this skill's Playwright loop.

## Workflow

1. **Run the routing check.** Decide whether the next build decision needs `$game-designer`, `$frontend-ux`, `$ux-writer`, `$communication-story-crafter`, or a Game Studio plugin skill. If yes, use the smallest useful pass and bring the result back into this implementation loop.
2. **Pick a goal.** Define a single feature or behavior to implement.
3. **Implement small.** Make the smallest change that moves the game forward.
4. **Ensure integration points.** Provide a single canvas and `window.render_game_to_text` so the test loop can read state.
5. **Add `window.advanceTime(ms)`.** Strongly prefer a deterministic step hook so the Playwright script can advance frames reliably; without it, automated tests can be flaky.
6. **Initialize progress.md.** If `progress.md` exists, read it first and confirm the original user prompt is recorded at the top (prefix with `Original prompt:`). Also note any TODOs and suggestions left by the previous agent. If missing, create it and write `Original prompt: <prompt>` at the top before appending updates.
7. **Verify Playwright availability.** Ensure `playwright` is available (local dependency or global install). If unsure, check `npx` first.
8. **Run the Playwright test script.** You must run `$WEB_GAME_CLIENT` after each meaningful change; do not invent a new client unless required.
9. **Use the payload reference.** Base actions on `$WEB_GAME_ACTIONS` to avoid guessing keys.
10. **Inspect state.** Capture screenshots and text state after each burst.
11. **Inspect screenshots.** Open the latest screenshot, verify expected visuals, fix any issues, and rerun the script. Repeat until correct.
12. **Verify controls and state (multi-step focus).** Exhaustively exercise all important interactions. For each, think through the full multi-step sequence it implies (cause → intermediate states → outcome) and verify the entire chain works end-to-end. Confirm `render_game_to_text` reflects the same state shown on screen. If anything is off, fix and rerun.
    Examples of important interactions: move, jump, shoot/attack, interact/use, select/confirm/cancel in menus, pause/resume, restart, and any special abilities or puzzle actions defined by the request. Multi-step examples: shooting an enemy should reduce its health; when health reaches 0 it should disappear and update the score; collecting a key should unlock a door and allow level progression.
13. **Check errors.** Review console errors and fix the first new issue before continuing.
14. **Reset between scenarios.** Avoid cross-test state when validating distinct features.
15. **Iterate with small deltas.** Change one variable at a time (frames, inputs, timing, positions), then repeat steps 8–14 until stable.

Example command (actions required):
```
node "$WEB_GAME_CLIENT" --url http://localhost:5173 --actions-file "$WEB_GAME_ACTIONS" --click-selector "#start-btn" --iterations 3 --pause-ms 250
```

Example actions (inline JSON):
```json
{
  "steps": [
    { "buttons": ["left_mouse_button"], "frames": 2, "mouse_x": 120, "mouse_y": 80 },
    { "buttons": [], "frames": 6 },
    { "buttons": ["right"], "frames": 8 },
    { "buttons": ["space"], "frames": 4 }
  ]
}
```

## Test Checklist

Test any new features added for the request and any areas your logic changes could affect. Identify issues, fix them, and re-run the tests to confirm they’re resolved.

Examples of things to test:
- Primary movement/interaction inputs (e.g., move, jump, shoot, confirm/select).
- Win/lose or success/fail transitions.
- Score/health/resource changes.
- Boundary conditions (collisions, walls, screen edges).
- Menu/pause/start flow if present.
- Any special actions tied to the request (powerups, combos, abilities, puzzles, timers).

## Test Artifacts to Review

- Latest screenshots from the Playwright run.
- Latest `render_game_to_text` JSON output.
- Console error logs (fix the first new error before continuing).
You must actually open and visually inspect the latest screenshots after running the Playwright script, not just generate them. Ensure everything that should be visible on screen is actually visible. Go beyond the start screen and capture gameplay screenshots that cover all newly added features. Treat the screenshots as the source of truth; if something is missing, it is missing in the build. If you suspect a headless/WebGL capture issue, rerun the Playwright script in headed mode and re-check. Fix and rerun in a tight loop until the screenshots and text state look correct. Once fixes are verified, re-test all important interactions and controls, confirm they work, and ensure your changes did not introduce regressions. If they did, fix them and rerun everything in a loop until interactions, text state, and controls all work as expected. Be exhaustive in testing controls; broken games are not acceptable.

## Core Game Guidelines

### Canvas + Layout
- Prefer a single canvas centered in the window.

### Visuals
- Keep on-screen text minimal; show controls on a start/menu screen rather than overlaying them during play.
- Avoid overly dark scenes unless the design calls for it. Make key elements easy to see.
- Draw the background on the canvas itself instead of relying on CSS backgrounds.

### Text State Output (render_game_to_text)
Expose a `window.render_game_to_text` function that returns a concise JSON string representing the current game state. The text should include enough information to play the game without visuals.

Minimal pattern:
```js
function renderGameToText() {
  const payload = {
    mode: state.mode,
    player: { x: state.player.x, y: state.player.y, r: state.player.r },
    entities: state.entities.map((e) => ({ x: e.x, y: e.y, r: e.r })),
    score: state.score,
  };
  return JSON.stringify(payload);
}
window.render_game_to_text = renderGameToText;
```

Keep the payload succinct and biased toward on-screen/interactive elements. Prefer current, visible entities over full history.
Include a clear coordinate system note (origin and axis directions), and encode all player-relevant state: player position/velocity, active obstacles/enemies, collectibles, timers/cooldowns, score, and any mode/state flags needed to make correct decisions. Avoid large histories; only include what's currently relevant and visible.

### Time Stepping Hook
Provide a deterministic time-stepping hook so the Playwright client can advance the game in controlled increments. Expose `window.advanceTime(ms)` (or a thin wrapper that forwards to your game update loop) and have the game loop use it when present.
The Playwright test script uses this hook to step frames deterministically during automated testing.

Minimal pattern:
```js
window.advanceTime = (ms) => {
  const steps = Math.max(1, Math.round(ms / (1000 / 60)));
  for (let i = 0; i < steps; i++) update(1 / 60);
  render();
};
```

### Fullscreen Toggle
- Use a single key (prefer `f`) to toggle fullscreen on/off.
- Allow `Esc` to exit fullscreen.
- When fullscreen toggles, resize the canvas/rendering so visuals and input mapping stay correct.

## Progress Tracking

Create a `progress.md` file if it doesn't exist, and append TODOs, notes, gotchas, and loose ends as you go so another agent can pick up seamlessly.
If a `progress.md` file already exists, read it first, including the original user prompt at the top (you may be continuing another agent's work). Do not overwrite the original prompt; preserve it.
Update `progress.md` after each meaningful chunk of work (feature added, bug found, test run, or decision made).
At the end of your work, leave TODOs and suggestions for the next agent in `progress.md`.

## Playwright Prerequisites

- Prefer a local `playwright` dependency if the project already has it.
- If unsure whether Playwright is available, check for `npx`:
  ```
  command -v npx >/dev/null 2>&1
  ```
- If `npx` is missing, install Node/npm and then install Playwright globally:
  ```
  npm install -g @playwright/mcp@latest
  ```
- Do not switch to `@playwright/test` unless explicitly asked; stick to the client script.

## Scripts

- `$WEB_GAME_CLIENT` (installed default: `$CODEX_HOME/skills/develop-web-game/scripts/web_game_playwright_client.js`) — Playwright-based action loop with virtual-time stepping, screenshot capture, and console error buffering. You must pass an action burst via `--actions-file`, `--actions-json`, or `--click`.

## References

- `$WEB_GAME_ACTIONS` (installed default: `$CODEX_HOME/skills/develop-web-game/references/action_payloads.json`) — example action payloads (keyboard + mouse, per-frame capture). Use these to build your burst.

## Project organization guardrail

Before creating or expanding game project files, consult the `work-management:project-structure` skill. Do not build expandable games as monolithic single-file implementations unless the user explicitly requests a one-off single-file deliverable.

For browser, Phaser, React Three Fiber, or Three.js games, keep entry files such as `src/main.js` thin. Separate core lifecycle, renderer, loop, scenes, entities, systems, UI/HUD, audio, config, assets, and docs before implementation when the game is expected to grow.
