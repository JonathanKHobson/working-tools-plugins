# Copy Patterns Reference

Pattern library for common UX copy moments. Each pattern includes when to use it, how to structure it, and what to avoid.

## Table of Contents

- CTAs and button labels
- Error messages
- Empty states
- Onboarding copy
- Confirmation dialogs
- Helper text and tooltips
- Success and confirmation messages
- Warning messages
- Loading states
- Navigation and labels

## 1. CTAs and Button Labels

### Primary action CTAs

Use for the single most important action on a screen.

Decision rule:

- Start with the shortest verb that stays clear in context.
- Add the object only when the object is ambiguous, the action is risky, or multiple actions compete on the same screen.
- Add extra context only when it materially improves information scent.

Examples:

| Context | Too much | Better |
| --- | --- | --- |
| Battle screen already names the run | Start battle run | Start |
| Edit form with one save action | Save changes | Save |
| Delete dialog names the item in body copy | Delete character | Delete |
| Upload flow with several file actions | Upload | Upload CSV |
| Checkout step that reveals the next stage | Continue | Review order |
| Pricing screen with a specific payment | Pay | Pay $29 now |
| Create surface with several object types | Create | Create campaign |

Rules:

- Keep primary CTAs to 1 to 4 words.
- Prefer context compression: if the heading, selected item, or prior step already names the object, do not repeat it in the button.
- Match the verb to what the user wants to do, not what the system does.
- Match tense to the moment.
- Test the button with the surrounding UI, not in isolation.

Anti-patterns:

- `Click here`
- `Submit` on most forms
- `Verb + object` when the object is already obvious
- Repeating screen titles, card titles, or selected item names in the CTA
- `OK` and `Cancel` as the only options in a confirmation dialog
- `Yes` and `No` for destructive actions

### Secondary and tertiary CTAs

Use for lower-stakes or exploratory actions.

Patterns:

- Learn more about `[X]`
- Get help
- Cancel
- Skip for now
- View details
- Dismiss
- Got it

## 2. Error Messages

### Four-part structure

1. What happened
2. Why it matters, only if non-obvious
3. What to do next
4. Escape hatch if helpful

### Pattern library

File and upload errors:

```text
[File type] couldn't be uploaded.
Files must be under [X] MB and saved as [format].
Try compressing the file or use a different format.
```

Connection or network errors:

```text
We couldn't connect to [service].
Check your internet connection and try again.
[Try again] [Contact support]
```

Permission errors:

```text
You don't have permission to [action].
Ask your [admin or team lead] to grant you access.
```

Validation errors:

```text
[Field name] needs a [description of valid input].
Example: [concrete example]
```

Session timeout:

```text
Your session timed out to keep your account secure.
Sign in again to continue where you left off.
```

Destructive action confirmation:

```text
Delete [item name]?
This can't be undone.
[Delete [item name]] [Keep it]
```

Always name the specific thing being deleted.

## 3. Empty States

### First-use empty state

Goal: orient the user, explain what will appear here, and point to the first action.

Pattern:

```text
[Short headline about what this space is for]
[One sentence about what appears after setup or creation]
[CTA to add the first thing]
```

Example:

```text
No campaigns yet
Create your first campaign to start tracking progress.
[Create campaign]
```

### Filtered or search empty state

Goal: acknowledge the miss and suggest what to try next.

Pattern:

```text
No [things] match "[search term]"
Try [suggestion 1] or [suggestion 2].
[Clear filters] [Search all [things]]
```

### Error empty state

Pattern:

```text
We couldn't load your [things].
[Reason if known]
[Try again]
```

Anti-patterns:

- Blank screens
- `No results` with no next step
- `Something went wrong` with no action
- Visible error codes

## 4. Onboarding Copy

### Welcome screen

Goal: orient, motivate, and move the user into the first real task.

Pattern:

```text
[Warm, specific welcome]
[One sentence on what they will accomplish]
[Primary CTA to start the first task]
[Optional secondary path]
```

Example:

```text
You're set up, [Name].
Start by creating your first [core object]. It takes about 2 minutes.
[Create your first [object]] [Take a quick tour]
```

### Progress copy

- Name each step by what the user accomplishes.
- Prefer `Step 2 of 4: Add your team` over `Step 2 of 4: User configuration`.
- Show concrete progress such as `2 more things to set up`.

### First-use tooltips and callouts

- Keep to one action per tooltip.
- Lead with the benefit, not the feature description.
- Keep to 2 lines max.
- Always include a dismiss path.

## 5. Confirmation Dialogs

### Destructive action

```text
Delete [specific thing name]?
This will permanently delete [thing] and [specific consequence]. You can't undo this.
[Delete [thing name]] [Keep [thing name]]
```

### Irreversible but recoverable action

```text
[Action] [thing]?
[Consequence]. [How to undo, if possible.]
[Action] [Cancel]
```

### Unsaved changes warning

```text
You have unsaved changes
Leave without saving?
[Leave without saving] [Keep editing]
```

Do not warn users before they try to leave. Warn at the decision point.

## 6. Helper Text and Tooltips

### Helper text

Use only when the label and placeholder still leave genuine ambiguity.

Patterns:

| Field | Anti-pattern | Better pattern |
| --- | --- | --- |
| Email | Enter your email address | We'll send your receipt here |
| Username | Enter a username | Visible to your team. Letters and numbers only. |
| Password | Enter a password | At least 8 characters, including one number |
| Budget | Enter your budget | Used to flag campaigns that may go over budget |
| Army name | Review this army and adjust the base to a role or advanced options if needed. | Remove, or move role rules to a tooltip if users miss them |

Anti-patterns:

- Restating the label
- Explaining backend behavior
- Explaining details users do not need to complete the task
- Narrating optional steps before the user needs them
- Filling space with text that does not change the next action

Use helper text for the smallest missing piece of information. If the content is optional, edge-case, or learnable on demand, move it out of the default view.

### Tooltips

Use for ambiguous icons, terms, or controls where the label alone is unclear.

Format:

- Noun phrase or one sentence
- Keep it short
- Trigger on hover or focus

Examples:

| Inline copy | Better approach |
| --- | --- |
| Advanced options let you fine-tune base role behavior, growth logic, and calculation overrides. | Inline label: `Advanced options` Tooltip: `Change role and override defaults.` |
| Auto-save keeps your changes between sessions and refreshes. | Remove inline note. Show `Saved` when it matters. |

If a tooltip needs click-to-open or several sentences, it is probably an information architecture problem.

## 7. Success Messages

Pattern:

Confirm what happened, then optionally give the next step.

Examples:

| Context | Anti-pattern | Better pattern |
| --- | --- | --- |
| Saved | Saved! | Changes saved |
| Sent | Success! | Message sent to [recipient] |
| Created | Created! | [Thing name] created - view it now |
| Deleted | Deleted. | [Item] deleted |
| Published | Published! | [Title] is live - View it |

Toast guidance:

- Show for 2 to 4 seconds
- Keep to one line
- Do not overuse exclamation points

## 8. Warning Messages

Goal: inform without threatening, and preserve user agency.

Pattern:

```text
[What is at risk]
[What the user can do before it happens]
[CTA or dismiss option]
```

Example:

```text
Your free trial ends in 2 days.
After that, your campaigns will be paused.
[Upgrade now] [Remind me later]
```

Guidance:

- Give specific timeframes when possible.
- Avoid alarmist wording.
- If every message is a warning, none of them feel meaningful.

## 9. Loading States

Never leave users with a blank screen.

Guidance by duration:

- Under 1 second: spinner or skeleton only, no copy needed
- 1 to 3 seconds: brief contextual message such as `Loading your campaigns...`
- 3 to 10 seconds: reason plus reassurance such as `We're crunching your data. This takes a moment.`
- Over 10 seconds: progress indicator plus an action such as `Still loading... [Cancel]`

Anti-patterns:

- Generic `Loading...` everywhere
- No feedback
- `Please wait` with no context

## 10. Navigation and Labels

Labeling principles:

- Use the user's vocabulary, not internal system vocabulary.
- Prefer noun labels for destinations and verb labels for actions.
- Test the information scent by reading the label aloud and asking whether it predicts the destination or outcome.

Examples:

| System thinking | User thinking |
| --- | --- |
| User Management | Your team |
| Content Repository | Your files |
| Notification Preferences | Notification settings |
| Account Parameters | Account settings |
| Campaign Configurations | Campaigns |

Sidebar and navigation anti-patterns:

- Deep nesting
- Icon-only navigation without labels
- Labels based on org charts or internal team structure instead of user goals
