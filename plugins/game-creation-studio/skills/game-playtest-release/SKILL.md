---
name: game-playtest-release
description: Use to plan and run game playtests, synthesize observed player behavior, triage issues, and verify a candidate build before a release decision.
---

# Game Playtest and Release

Tie the session to one consequential decision, such as whether new players understand the goal, can use the controls, or want another run. Use a build that can complete the intended run.

1. Record build identifier, platform, device, controls, scenario, and test question. Choose a task a player can attempt without coaching. Get appropriate consent for recording, telemetry, or sharing; keep sensitive player information out of public issue logs.
2. Observe what the player does, says, retries, and abandons. Separate direct observations from interpretations. Let the task play out before explaining controls unless safety or access requires intervention.
3. Log issues with reproduction steps, expected and actual behavior, severity by blocked player outcome, and a visual or technical receipt when available. Count repeated patterns but retain individual context; a small convenience sample is not a population estimate.
4. Test the strongest alternate explanation for a problem. For example, a player failing a jump may reflect unreadable timing cues, input latency, or level geometry. Choose one discriminating next run or instrumentation change.
5. Prioritize fixes that block the core loop, crash, lose progress, prevent access, or violate a release promise. Re-run the affected path and neighboring states after a fix. For a browser game, hand QA execution to official OpenAI Game Studio's `game-playtest` and use the engine specialist for implementation.
6. For a release candidate, verify the exact artifact, install or launch path, start-to-end run, controls, critical states, asset licenses, performance on target hardware, and any platform submission requirements. Check the actual published/downloadable state only if release is authorized. Record remaining known issues and rollback path.

Deliver a finding table with observation, evidence, impact, hypothesis, and next check, followed by a release recommendation tied to explicit acceptance criteria. Distinguish built, tested, submitted, published, and player-received states. A local clean run is not a store approval or public release.
