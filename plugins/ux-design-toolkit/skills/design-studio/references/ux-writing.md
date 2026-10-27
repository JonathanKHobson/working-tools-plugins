# UX writing

Write for the user's next decision. Start with the action, outcome, and state, then choose words that match the product's domain and the user's vocabulary. Preserve exact factual terms, names, and constraints. Shorter is useful only when it improves recognition or scanning.

Before adding copy, inspect what the rendered layout, controls, labels and state already communicate. Give each remaining message a location: essential to the current decision; needed at the action or error; useful on request; or internal to production. Keep the first two at the point of need, make secondary detail easy to find, and keep internal deliberation out of the interface. Do not explain an abandoned design choice to a user who never encountered it.

Use progressive disclosure for useful secondary detail, with a clear label and route back. Keep fees, irreversible consequences, eligibility, privacy choices and necessary recovery information visible before the relevant action. Do not hide essential meaning in a tooltip, placeholder or an unlabeled icon. Removing words must preserve what users need, including accessible names.

For a control, make the verb and object clear when context is weak: “Save changes” is more informative than “Submit.” For destructive or consequential actions, state the consequence before confirmation. For errors, tell the user what happened, whether work was preserved, and one useful recovery action. For empty states, explain why nothing is shown and what the user can do next; avoid promising results the system cannot deliver. For permission or loading states, describe the real state rather than making the interface sound conversational for its own sake.

Check labels across sibling screens, navigation, dialogs, and notifications. One operation should not acquire several names by accident. Ensure text still works in the layout at narrow width, high zoom, and with localization expansion. Keep labels visible when a field has a value; placeholder text is supplementary guidance.

For a copy-only request, use the current UX-writing specialist if available and return the revised copy directly. For copy tied to layout or behavior, hand the final wording to the owning UI surface and verify it in the rendered state. Promotional copy for posters and ads follows the graphic-design route because space, hierarchy, and legal facts shape it.

Load and apply the installed `writing-quality-studio:natural-prose-editor` skill, the everyday Humanizer, to the exact final wording within these state and layout constraints. Follow its review-recording handoff; naming the skill is not a completed review. If it is unavailable, review the wording directly and report the missing specialist. During rendered review, ask whether each visible explanation adds decision-relevant meaning beyond the design, and whether users can find the next action and its consequence. A clean text extraction cannot prove placement works.

When the cause or next action is unknown, do not invent one. Use neutral wording or give a clearly conditional variant. A standalone sentence rewrite does not require rendered anchors; check the requested wording against the supplied facts and scope.

When a layout demands equal-length copy or a fixed number of items, preserve the actual entities, facts and qualifications first. Adjust the container with its owner if accurate copy cannot fit. Parallel labels may aid comparison; do not vary terminology merely to appear less formulaic. Use the [conditional design method](../../design-review/references/intentional-design.md) only when layout or implied capability is the concern.

Method reference: [Nielsen Norman Group, Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/). It supports separating primary and secondary needs and making the route to detail apparent; it does not establish that any particular layout has passed user testing.
