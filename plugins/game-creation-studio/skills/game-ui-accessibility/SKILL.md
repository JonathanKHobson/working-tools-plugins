---
name: game-ui-accessibility
description: Use to design or inspect game HUD, menus, controls, onboarding, state feedback, and accessibility across keyboard, pointer, controller, touch, and assistive use.
---

# Game UI and Accessibility

Inspect the game's actual rendered screen and controls, plus its source components, before changing a visual direction. Map 3 to 8 anchors: viewport or screen, approximate region, UI element, observed fact, intended action. Verify the same anchors after the change.

1. Follow the player's task through title/start, active play, pause, success, failure, settings, and restart. For each state, identify the primary action, required information, and feedback. Keep HUD information close to the decision it supports and avoid covering play-critical space.
2. Trace each input modality the game claims to support. Check discoverability, focus order, input remapping or alternatives where relevant, and recovery from lost focus. Make interactions operable without relying solely on precise pointer timing or color distinction.
3. Check text scale, contrast in real game imagery, labels, icon meaning, motion/flash alternatives, audio captions or visual cues, and persistent settings where applicable. Test key states under actual target viewport and input device conditions; an accessibility checklist alone is not proof of use.
4. Let a new player start and complete the first action. Observe confusion before adding tutorial copy. Prefer feedback tied to the action; give optional instruction only for controls or goals the scene cannot communicate.
5. After changes, compare rendered states, test input and focus paths, and run at least one player task. Report what was observed, what was inferred, and any device or modality not tested.

For browser UI implementation, route to official OpenAI Game Studio's `game-ui-frontend`; its `game-playtest` owns browser QA. Use the owning game's design tokens and component patterns. Deliver revised states or code plus the anchor map, input matrix, and observed task result. Do not call a source-only check visual QA.
