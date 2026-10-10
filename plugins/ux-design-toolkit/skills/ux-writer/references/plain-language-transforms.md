# Plain Language Transforms

Before-and-after examples for turning technical, jargon-heavy, or over-explained UI copy into clear, user-centered language.

## Table of Contents

- Developer or technical jargon
- System behavior announced too early
- Over-explaining obvious controls
- Repeated-context CTAs
- Abstract nouns to active verbs
- Passive voice to active voice
- Enterprise language
- Settings and configuration copy
- Game and simulation UI language
- Status and state language
- Form and validation language
- Remove or defer instead of rewriting

## 1. Developer or Technical Jargon Exposed to Users

These terms belong in code comments or internal docs, not user-facing UI.

| Before | After | Note |
| --- | --- | --- |
| Runtime-only empty session placeholders are not persistent across refresh. | Remove | Internal system note |
| In-product field manual for onboarding, CSV requirements, settings, and definitions | Help or Field guide | Name the user need, not the inventory |
| Null value returned | Nothing found | Replace code language with outcome language |
| API rate limit exceeded | You've made too many requests. Wait a minute and try again. | Translate the cause into user guidance |
| Session token expired | You've been signed out. Sign in again to continue. | Describe the effect |
| Async operation in progress | Show loading state | Solve with design, not prose |
| Config file not found | We couldn't load your settings. Try refreshing the page. | Plain outcome plus next step |
| Index out of bounds | Something went wrong. Try again or contact support. | Do not expose internals |
| Deprecated feature | This feature is being phased out. Learn what's replacing it. | Explain impact |
| Regex validation failed | That doesn't match the expected format. Example: [example] | Show the expectation |

## 2. System Behavior Pre-Announced to Users

These are things the system already handles. Explain them only at the moment they matter.

| Before | After | Note |
| --- | --- | --- |
| Leave the settings tab or refresh with unsaved settings will change will warn before loss. | Remove | Warn on navigation, not before |
| The system will automatically log you out after 30 minutes of inactivity for security purposes. | Still there? Sign in to continue. | Trigger at timeout moment |
| All changes are auto-saved every 5 seconds. | Show a Saved indicator | Show, do not narrate |
| Your data will be encrypted in transit using AES-256 encryption. | Your data is secure. | Use trust language only where needed |
| Browser caching may cause your view to be out of date. | Use refresh indicator or auto-refresh | Solve through UX |
| Changes are staged and will not take effect until you click Save. | Save and apply changes | Move the explanation into the action |
| Advanced options are available if you need more control over role behavior. | Move to tooltip or advanced section | Offer it when the user reaches that decision |

## 3. Over-Explanation of Obvious Controls

Do not explain conventions users already understand.

| Before | After | Note |
| --- | --- | --- |
| Click the X button to close this dialog | Remove | Trust the user |
| Use the scroll bar on the right to scroll through results | Remove | Never explain standard scrolling |
| Click the checkbox to select this item | Remove | Checkbox behavior is obvious |
| Open the help wiki for troubleshooting documentation and FAQs, guides, and definitions | Help | The label already carries the scent |
| Press Enter to submit your search query | Remove in most contexts | Standard search behavior |
| This field is required (marked with *) | Required or * in label | Use the convention consistently |
| Your password must be kept secret and not shared | Remove | Obvious and condescending |

## 4. Repeated-Context CTAs

When the screen, card, dialog, or prior step already names the object, do not repeat it in the action label.

| Before | After | Note |
| --- | --- | --- |
| Start battle run | Start | The battle context is already on screen |
| Save changes | Save | Use the shorter verb when there is only one save action |
| Delete character | Delete | In a delete dialog, the object belongs in the body copy |
| Create new campaign | Create campaign | Keep the object only if several object types are possible |
| Continue to review order | Review order | Name the destination when it clarifies the next step |

Rule:

Start with the shortest verb that stays clear in context. Add the object only when clarity would drop without it.

## 5. Abstract Nouns to Active Verbs

Nominalizations make UI copy heavier than it needs to be.

| Before | After |
| --- | --- |
| Make a selection | Select or Choose |
| Provide an indication of | Show or Tell us |
| Give consideration to | Consider |
| Perform a review of | Review |
| Make a decision | Decide |
| Provide a description of | Describe |
| Perform an update | Update |
| Initiate the process | Start |
| Complete the configuration | Set up |
| Engage in exploration | Explore |
| Submit your application | Apply |
| Effect a change | Change |
| Facilitate the upload | Upload |

## 6. Passive Voice to Active Voice

Passive voice often hides the actor and weakens the instruction.

| Before | After |
| --- | --- |
| Your file was uploaded successfully | File uploaded or You uploaded [filename] |
| An error was encountered | Something went wrong |
| Settings have been saved | Settings saved |
| Your account has been created | Account created - welcome aboard |
| Changes will be applied when saved | Save to apply changes |
| Access has been denied | You don't have access to this |
| Your password has been reset | Password reset - sign in with your new password |
| No items were found | We didn't find anything matching "[term]" |

## 7. Enterprise or Corporate Speak

Professional-sounding language often hides meaning.

| Before | After |
| --- | --- |
| Leverage our platform's capabilities | Use [specific feature] |
| Optimize your workflow | Work faster or Skip the manual steps |
| Utilize the dashboard | Use the dashboard |
| Onboarding experience | Getting started |
| Next-generation solution | Name the actual thing it does |
| Seamless integration | Connects with [X] in one click |
| Best-in-class | Remove or state a concrete benefit |
| Actionable insights | Spot trends, act faster |
| End-to-end visibility | See everything from [X] to [Y] |
| Pain points | Never use in UI copy |
| Touch base | Contact or Reach out |

## 8. Settings and Configuration Language

Settings pages are common failure zones for UX writing.

| Before | After | Note |
| --- | --- | --- |
| Enable notifications | Send me notifications | User-voice framing feels more controllable |
| Disable auto-save | Turn off auto-save | Turn off is more universal than disable |
| Configure display preferences | Display settings | Shorter and clearer |
| Modify account parameters | Account settings | Remove corporate phrasing |
| User interface density settings | Compact view or Comfortable view | Show meaning, not jargon |
| Advanced configuration options | More settings | Less intimidating |
| Notification frequency parameters | How often to notify you | Phrase by user need |
| Default behavior settings | Default settings | Cut filler |
| System-level preferences | Advanced | Do not expose architecture |
| Persistence settings | Save across sessions | Translate to user impact |

## 9. Game and Simulation UI Language

Preserve intentional domain terms. Simplify the surrounding UI framing.

| Before | After | Preserve? |
| --- | --- | --- |
| Initiative modifier calculator | Initiative calculator | Trim filler only |
| Runtime dice probability seed | Remove | Internal system term |
| Ability score application configuration | Ability score settings | Simplify noun stack |
| Combat action queue management | Combat actions | Simplify label |
| Open the in-product field manual | Open field guide or Help | Trim wrapper language |
| Session state persistence | Auto-save or Save between sessions | Translate the function |
| Dice math breakdown | Dice breakdown or How this was calculated | Preserve domain term, add clarity |
| Encounter difficulty threshold | Difficulty setting | Only if threshold adds no real user value |
| CR modifier override | Keep CR modifier if CR is domain vocabulary | Preserve intentional game language |
| Review this army and adjust the base to a role or advanced options if needed. | Remove, or split into `Role` tooltip plus `Advanced options` help text | Move optional guidance out of the default view |

Rule:

Keep names of mechanics, classes, game systems, and community-standard terms when users are expected to learn them.

## 10. Status and State Language

Communicate what is happening now with the smallest useful amount of text.

| State | Before | After |
| --- | --- | --- |
| Loading | Loading... | Loading your [things]... |
| Saving | Saving... | Saving... |
| Saved | Your changes have been saved to the system. | Saved or Changes saved |
| Syncing | Synchronization in progress | Syncing... |
| Offline | Network connectivity unavailable | You're offline - changes will save when you reconnect |
| Updated | The data has been refreshed successfully. | Updated just now |
| No changes | No modifications have been detected. | Remove or Up to date |
| Failed | Operation failed. Error code: 500. | Something went wrong. Try again or contact support. |

## 11. Form and Validation Language

### Field labels

| Before | After |
| --- | --- |
| First Name (Required) | First name * |
| Enter your date of birth in MM/DD/YYYY format | Label: Date of birth. Placeholder: MM/DD/YYYY |
| Please provide the email address associated with your account | Email |
| Select one (1) option from the following | Choose one |
| Input the quantity desired | Quantity |

### Validation messages

| Before | After |
| --- | --- |
| This field cannot be blank | [Field name] is required |
| Invalid email address format | Enter a valid email, like name@example.com |
| Value must be between 1 and 100 | Enter a number between 1 and 100 |
| Passwords do not match | Passwords don't match - try retyping |
| Username already taken | That username is taken. Try [suggestion]? |
| Request failed | We couldn't save this. Try again? |

## 12. Remove or Defer Instead of Rewriting

Some copy is accurate but still wrong for the current moment. Remove it from the default view or defer it to when the user needs it.

| Before | After | Why |
| --- | --- | --- |
| Review this army and adjust the base to a role or advanced options if needed. | Remove from inline helper text. Add tooltip only if users miss role setup. | The sentence adds load without improving the next action |
| Auto-save keeps your current selections between sessions and page refreshes. | Remove. Show `Saved` or recovery messaging only when relevant. | The user does not need the implementation upfront |
| You can update these settings later in the advanced configuration section. | Move to secondary help or advanced section intro. | Optional path, not a primary-task instruction |
| Runtime-only placeholders are cleared on refresh. | Remove | Internal behavior, not user guidance |
