# Technical writing

Read this reference when the output is documentation, a tutorial, a how-to guide, a runbook, API or code-related prose, release notes, interface instructions, or another artifact that readers must scan and act on.

The user's goal and project conventions still take priority. Do not impose documentation conventions on code, exact quotations, schemas, or a required template.

## Define the document's job

Give the document one primary purpose. A task page can contain supporting concepts, but its title and main path should match the task. A concept page can link to procedures instead of hiding a tutorial inside an overview.

Make the outcome and prerequisites apparent from the title or opening. Add an introduction only when it contributes information that the title and surrounding context do not. Put consequential warnings and prerequisites before the action that depends on them. Keep optional background off the critical path.

Prefer prescriptive documentation when one path fits most readers. Recommend that path and explain the decision-changing exceptions. Do not present a menu of equal-looking choices when the reader wants to complete a task.

## Organize for scanning

Use a unique level-1 title. Follow a logical heading hierarchy and do not skip levels. Headings must help readers distinguish sections when seen alone in a table of contents or screen-reader outline.

Use sentence case. Start a task heading with a base-form verb when practical:

- `Create an access token`
- `Restore a backup`

Use a noun phrase for a concept:

- `Token lifetime`
- `Backup retention`

Avoid generic headings such as *Overview*, *Details*, *Considerations*, and *More information* when a specific heading is possible. Do not repeat the page title as the first section heading.

Give each paragraph one main idea. Put the point that distinguishes the paragraph first. Keep qualifications next to the claim they limit. A paragraph longer than five or six sentences deserves review, but a single coherent idea can justify a longer paragraph.

## Choose a list or table

Use a numbered list when order, rank, or priority matters. Use bullets for a nonsequential collection. Use a description list for terms paired with definitions. Use a table when readers need to compare the same properties across several items.

A one-item list is rarely useful, but it can fit a required template or set off a single action, warning, or checklist item. Introduce a list with a complete sentence when the heading does not provide enough context. Make list items parallel: the same grammatical form, capitalization pattern, and punctuation logic.

Start list items with a capital letter unless case carries technical meaning. End complete sentences with punctuation. Short labels, code-only items, and phrases without verbs usually do not need periods. If punctuation becomes inconsistent, rewrite the items to make their structure consistent.

Avoid ending an inline list with *etc.* or *and so on*. Introduce it as examples if it is intentionally incomplete.

Use a table only when it makes a relationship clearer. Introduce the table in the preceding prose. Use real row and column headings, avoid merged cells, and do not rely on an icon or color alone to convey a value.

## Write procedures

Use a numbered list for a sequence with two or more steps. A single action usually works as a sentence or bullet instead of a one-item numbered procedure.

Introduce the procedure only when the title or surrounding text does not provide enough context. Use a complete sentence, not a fragment completed by the steps.

Write steps in the order the reader performs them. In each step:

1. Start the first sentence with an imperative verb.
2. Put the tool, page, field, or environment before the action when readers need that context.
3. Put the goal before the action when it explains why the step exists.
4. Keep one decision or substantial action in the step.
5. Put an immediate result after the action when readers need it to verify or continue.
6. Put a brief justification after the action when it prevents a likely mistake.

Examples:

- `In the console, open **API access**.`
- `To keep the existing token active, select **Add token**.`
- `Store the recovery code in a secure location. You can't display it again.`

Mark an optional step with `Optional:` at the beginning. Put a warning before the risky action, not after it.

Prefer the shortest accessible method. If the document needs several methods, separate them under clear headings or tabs, recommend a default, and do not interleave their steps.

Do not repeat a procedure in several places. Link to the canonical procedure and provide the short context a reader needs before following the link.

## Present commands and code

Say what a command accomplishes when that context adds information:

- Better: `Create the production configuration:`
- Weaker: `Run the following command:`

When the purpose is already clear, a direct introduction such as *Run this command* can be the least distracting choice.

Put a command or code sample directly after its introduction. Explain placeholders close to the sample and use a consistent, recognizable placeholder style. Do not use realistic secrets, credentials, or unsafe domains as sample data.

Show output only when readers need it to verify success, diagnose a result, or perform the next step. Label output clearly and do not mix it with commands readers should copy.

Use code formatting in prose for items such as these:

- Commands, flags, subcommands, and arguments.
- Class, method, function, and variable names.
- Filenames, paths, extensions, and configuration keys.
- HTTP methods and status codes.
- Literal values, placeholders, and text the reader enters.
- Short console output and error strings.

Do not use code formatting for product names, ordinary technical terms, URLs used as links, or emphasis. Preserve the exact spelling and case of code elements. Add a descriptive noun when it improves grammar: *the `config.yaml` file*, *the `--force` flag*, *the `CreateUser` method*.

Keep examples focused on the decision being taught. Include enough realistic context to prevent copying errors, but remove incidental complexity. Explain the part that matters instead of paraphrasing every visible line.

## Describe interfaces

Refer to a control by its visible label or accessible name. Match the interface's capitalization, but omit decorative punctuation such as an ellipsis when it is not needed to identify the control.

When the format supports it and the project follows this convention, use bold for clickable or selectable interface labels. Use code formatting for text the reader enters.

Put the interface location before the action:

- `In **Settings**, select **Notifications**.`

For sequential menu choices, use the project's established separator and make the reading order accessible. Do not rely on *above*, *below*, *on the left*, color, shape, or an unlabeled icon to orient the reader. If a control is difficult to locate, provide a labeled screenshot or its accessible name.

Describe what the software does in third person and what the reader does in second person or the imperative:

- `Select **Save**. The application validates the configuration.`

## Link with a purpose

Give readers short, essential context on the current page. Link to material that supplies depth, evidence, a canonical procedure, or documentation for another system.

Choose the most relevant destination, preferably the exact section. Use the page title or a short descriptive phrase as link text. The link text should make sense when read without the surrounding sentence.

Avoid vague link text such as *click here*, *this page*, and *read more*. Avoid a bare URL when normal link text is possible. Explain unexpected behavior such as a file download, email action, or forced new window.

Do not repeat the same link several times on a short page or offer several links that do the same job. Each link creates a choice and a chance for the reader to lose their place.

## Make the document durable

Describe current behavior in present tense. Avoid *currently*, *now*, *new*, *latest*, *soon*, and similar markers when the document is meant to stay accurate. Use a date or version when the comparison with an earlier state matters.

Time-relative language is appropriate in release notes, announcements, migration notices, deadlines, incident reports, and procedures where a state changes after an action.

Do not promise an unreleased capability or strategy without explicit authority. Distinguish a committed date from a target or possibility.

Use one term and capitalization for each concept. Define abbreviations on first use unless the audience certainly knows them. Prefer unambiguous dates and include a time zone when readers in different regions could act on the time.

## Write accessibly

Use descriptive titles and a logical heading hierarchy. Do not create empty headings or use visual styling in place of semantic structure.

Provide useful alternative text for an informative image and empty alternative text for a purely decorative image. Do not introduce essential information only in an image, animation, audio track, or video. Provide captions, transcripts, or nearby text as appropriate.

Make the content understandable without color, sound, images, position, or punctuation. Add a text label or another cue when color or an icon communicates state.

Do not center or fully justify body text in a rendered document. Avoid forced line breaks inside prose. Use native semantic elements before custom controls when authoring HTML.

Test interactive documentation with a keyboard. When the artifact's risk or audience justifies it, test with a screen reader and at enlarged text sizes.

## Apply formatting consistently

Follow the user's, author's, or project's regional style. Preserve the source dialect when editing. Use American English spelling, punctuation, and the serial comma only when no other convention applies.

Use bold mainly for interface elements and short run-in headings. Use italics sparingly for emphasis, terms as terms, or titles that require them. Do not underline for emphasis. Use semantic Markdown or HTML rather than manual font changes.

Use sentence case for headings and navigation. Avoid all capitals except where case is part of an exact technical item or an established placeholder convention.

Use punctuation to expose sentence structure, not to create a signature voice. Prefer a period over a semicolon when two independent thoughts are easier to read separately. Use parentheses for genuinely secondary information; move important conditions into the main sentence.

## Check the finished artifact

Confirm all of the following:

- A reader can identify the page's job from its title and opening.
- Prerequisites and warnings appear before the actions that depend on them.
- The recommended path is visible and complete.
- Steps contain actions in execution order.
- Commands, code, placeholders, output, and interface labels are exact and distinguishable.
- Headings, lists, tables, and links work when scanned out of context.
- Terminology and capitalization are consistent.
- Claims remain true for the stated scope and version.
- The document conveys its information without relying on one sensory or visual cue.
