# UX Writing Reference

Use this file when frontend code includes labels, helper text, errors, confirmations, empty states, or inline guidance.

## Core principles

- Write copy to help the user act, recover, decide, or understand.
- Prefer plain language over system jargon.
- Keep terminology consistent across the interface.
- Use placeholders as examples only, never as the sole label.

## Labels and buttons

- Use sentence case.
- Prefer specific nouns users already recognize.
- Start button labels with a clear verb when possible.

Examples:

- `Save changes`
- `Create project`
- `Delete account`
- `Send message`

Avoid generic labels like `OK`, `Submit`, `Yes`, and `No` when a more specific action is possible.

## Error messages

Good error messages answer three questions:

1. What happened?
2. Why does it matter?
3. What should the user do next?

Patterns:

- `Enter a valid email address, like name@example.com.`
- `We couldn't save your changes. Check your connection and try again.`
- `You don't have permission to view this. Ask your admin for access.`

Avoid:

- raw status codes as the main message
- blameful wording
- vague messages with no recovery path

## Empty states

An empty state should include:

- what is missing
- why the space is empty, when helpful
- the next useful action

Patterns:

- `You haven't added any projects yet. Create your first project to organize your work.`
- `No tasks match these filters. Clear a filter or adjust the date range.`
- `Nothing to show here. You may not have access to items in this section.`

## Loading and success states

- For brief loads, a spinner or skeleton may be enough.
- For longer waits, say what is happening.
- After a user-triggered action, confirm the outcome briefly.

Patterns:

- `Loading your dashboard...`
- `Saving...`
- `Changes saved`
- `Message sent to Sarah`

## Confirmation dialogs

Use the action in both the title and the primary button label.

Pattern:

- Title: `Delete this workspace?`
- Body: `All projects, files, and team members will be permanently removed. This can't be undone.`
- Actions: `Keep workspace` and `Delete workspace`

Avoid generic confirmation patterns like `Are you sure?` with `Yes` and `No`.

## Inclusive and accessible copy

- Avoid idioms and culture-specific phrasing when the audience is broad.
- Keep reading complexity appropriate for the product audience.
- Do not rely on color words alone to explain a state.
- Make inline instructions persist outside placeholders when they are important.

## Review checklist

- Does the label tell the user what this is?
- Does the button say what happens next?
- Does the error explain recovery?
- Does the empty state offer a path forward?
- Is the wording consistent with the rest of the interface?
