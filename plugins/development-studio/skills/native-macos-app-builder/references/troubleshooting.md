# Troubleshooting

## Triage order

Classify the failure before changing code:

1. compile error
2. linker error
3. signing or entitlement error
4. runtime crash or broken behavior
5. SwiftUI preview failure
6. sandbox or file-access issue
7. packaging or notarization failure

Fix the narrowest root cause first.

## Compile and linker issues

Check:

- missing imports
- unavailable APIs for the deployment target
- symbol visibility or duplicate definitions
- target membership for new source files
- package resolution or package version drift

Linker problems often come from wrong target membership, missing frameworks, or mismatched package products.

## Project configuration issues

Inspect:

- `Info.plist` keys and generated plist settings
- bundle identifiers
- deployment target mismatches
- scheme and configuration selection
- signing team and certificate selection

Do not assume the selected Xcode scheme matches the intended target.

## SwiftUI preview failures

Common causes:

- preview code touching unavailable runtime dependencies
- incorrect `@MainActor` or concurrency usage
- missing environment objects
- package resolution failures
- deployment target or SDK mismatches

Reduce the preview to the smallest failing view before changing surrounding code.

## Runtime and concurrency issues

- Keep UI updates on the main actor.
- Avoid pushing long-running work into views.
- Check task cancellation, actor isolation, and re-entrancy around state changes.
- When behavior is intermittent, inspect async boundaries before rewriting UI code.

## Sandbox and file access issues

- Verify the entitlement set matches the requested behavior.
- Confirm the app is using user-initiated file selection when sandboxed.
- Persist security-scoped access only when necessary and release it correctly.
- Distinguish between a missing entitlement and a missing user-granted permission path.

## AppKit bridge issues

When SwiftUI bridges into AppKit, check:

- representable lifecycle methods
- coordinator wiring
- delegate ownership
- focus and responder-chain handoff
- window or view assumptions that are only valid after attachment

If only one bridge component fails, isolate it instead of rewriting the screen around it.

## Repair stance

- Preserve the current app shape unless it is the root cause.
- Prefer targeted fixes over broad rewrites.
- Explain structural problems briefly when the codebase is fighting macOS conventions.
