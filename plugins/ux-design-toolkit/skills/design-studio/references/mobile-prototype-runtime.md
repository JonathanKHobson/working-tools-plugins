# Mobile prototype runtime contract

Use when a requested deliverable is an interactive phone simulation in a browser, including simulated keyboard, device frame or gestures. This differs from a responsive webpage and from a native iOS/Android app. UX owns task, source, composition and verification. The actual selected runtime owns its implementation, assets, interfaces, integrity checks and packaging. This document is original receiving-owner guidance, not a bundled emulator or copied runtime.

## Select the actual output

A simple narrow web flow can use the incumbent web stack. An interactive phone simulation needs a real simulator/runtime contract. A native app needs its native build owner. Do not substitute one for another merely because all have a mobile-width screenshot. Clarify only when the intended output materially changes the next step.

The official OpenAI Product Design distribution, when legitimately installed and callable on the receiving host, supplies web and mobile prototype starters and a local bootstrap/runtime. This is a specific implementation capability, not a normal prerequisite for UI/UX reasoning. For a selected Product Design mobile starter, read its current complete local-prototype-preflight reference, mobile template AGENTS.md, component guide, runtime lock/check scripts and relevant tests from that installed package. Resolve its path through current discovery, verify version/tool availability and use its supported bootstrap rather than copying its source into UX. Follow an explicitly invoked Product Design workflow in full. If unavailable, use another verified runtime only if it satisfies the requested output; report a missing simulator plainly rather than claiming a responsive page is equivalent.

## Preserve and adapt the selected runtime

Before editing, record the app-owned entry files, protected runtime files, component APIs, screen geometry, safe-area/keyboard conventions, assets, scale, navigation and preview/build commands. Treat these as the runtime's actual contract, not a universal API. Product Design's installed starter separates app screen/style files from protected phone/keyboard/scroll/navigation infrastructure and supplies a runtime-integrity check; read the current paths and commands before use. Never weaken a check just to pass a handoff. An authorized runtime modification requires its own changed-contract verification and lock update through the runtime owner's procedure.

Build the app's own content and state inside the designated boundary. Keep device chrome (frame, camera/status/navigation/home indicator) separate from app content. Preserve live versus mock time according to the brief. Device changes should retain valid app state. When a reference omits or differs from device chrome, match app content without rasterizing a second status bar or removing infrastructure silently.

## Interaction requirements

Check actual supported components and the following behaviors; adapt them through the runtime's documented API:

- Screen navigation preserves app state as promised, hides/dismisses keyboard where needed and keeps device chrome fixed while content transitions.
- A route header/footer's content inset matches whether the runtime reserves space or overlays it. Final content and actions must scroll clear of fixed app controls and actual device safe areas.
- Keyboard-linked fields and composers share one inset/visibility source. Opening a modal/sheet or closing a composer dismisses the keyboard in the same transition. Moving focus between text fields can preserve a session; blur to non-input content clears it where the contract requires.
- Horizontal rails and vertical content resolve gesture direction once. A completed drag must not activate a card/button; vertical intent over a horizontal rail must still scroll its parent. Avoid conflicting native and custom scroll/snap/gesture owners.
- Scroll release/momentum and edge behavior stay with the runtime. Prevent unintended browser image/file dragging only inside the simulation's owned surface; do not interfere with unrelated app behavior.
- Sheets/menus render in the phone's intended portal/layer, have supported dismissal/focus behavior and complete their entrance/exit without losing state prematurely.

For different iOS/Android presets, test real runtime dimensions and platform inset conventions rather than assuming one bottom-padding value. Native hardware/assistive-technology claims remain separate; a browser simulation verifies only its simulated path.

## Preview, fidelity and hosting

Run the runtime's integrity check before accepting the preview and before handoff if it has one. Use its normal preview command and the current host browser route from [prototyping](product-prototyping.md). Inspect the full stage for usability, then capture unscaled app content for [design comparison](design-comparison-qa.md). Record actual screen CSS bounds, image pixels and scale. Check a text-entry/composer transition, a navigation/back path, horizontal/vertical gesture conflict, drag click suppression, sheet dismissal and device switch as relevant.

If the selected Product Design starter is shared through Sites, retain that starter and follow its current Sites packaging/tests: client output, worker/server entry, metadata and route fallback are real build contracts. Do not reinitialize it with another Site scaffold or replace its phone runtime to host it. Read the actual receiving Sites hosting procedure and inspect generated files/tests through the selected runtime. For another runtime or host, use its equivalent contract rather than inventing these filenames. Confirm deep-link fallback preserves app routes without converting missing API/write requests into successful shell responses.

Acceptance requires the requested simulation running, protected runtime intact, app-owned source fidelity, relevant interactions observed and the requested preview or hosted URL accessible. Missing runtime/browser/hosting limits are explicit. Actual provider source/assets remain in their legitimate installed owner; none are copied or relicensed here.
