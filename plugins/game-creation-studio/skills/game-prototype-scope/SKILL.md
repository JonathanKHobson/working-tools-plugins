---
name: game-prototype-scope
description: Use to scope a small playable game prototype or vertical slice, define a cut list, milestones, project structure, and the first end-to-end test.
---

# Game Prototype Scope

Anchor the scope to one named question about the core loop. Consult the owning project's map and existing engine before creating files. An engine decision is needed only if none exists; use official OpenAI Game Studio's `game-studio` and `web-game-foundations` for browser stack choice.

1. Define a complete run: start, one meaningful choice, feedback, success or failure, and restart or exit. Choose one target device and input method. Record the time box and actual people/tools available.
2. List indispensable mechanics, UI states, and temporary assets needed to complete that run. Use placeholder art when art fidelity is not the question; choose representative art when readability, animation, or mood is the question.
3. Split work into a playable first pass, one evidence pass, and only then polish. Each pass has an observable acceptance check, such as "a fresh player can finish or fail without developer intervention." Keep the entrypoint thin and use the project's existing scene/system/UI conventions.
4. Write a cut list of features that do not affect the named question. If a new feature is proposed, name the current item it displaces within the time box.
5. Identify the riskiest dependency and test it early: input latency, camera, networking, procedural layout, asset import, or save path. Do one small proof before building a larger content pipeline.
6. At the end of the first playable pass, run it on the target device and record the exact build, controls, route, errors, and visual state. Route player observation to [playtest release](../game-playtest-release/SKILL.md).

Deliver a one-page slice contract: target question, run path, acceptance checks, cut list, owner and next executable action. Do not make a speculative roadmap a prerequisite for the first run. A project that launches is not yet a complete playable slice; verify the start-to-end path.
