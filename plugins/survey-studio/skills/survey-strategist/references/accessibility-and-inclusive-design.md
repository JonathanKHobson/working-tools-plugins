# Accessibility and Inclusive Design

## Goal

Make the survey perceivable, operable, understandable, and robust across assistive technologies, devices, languages, literacy levels, cognitive styles, and situational constraints.

## Semantic structure

- Give every control a persistent programmatic label.
- Group related radio/checkbox controls with a fieldset and legend or equivalent.
- Associate help, constraints, required status, and errors with the field.
- Use headings in a logical hierarchy and landmarks for navigation.
- Announce dynamic content and validation changes appropriately.
- Preserve a meaningful reading/focus order.

## Interaction

- Full keyboard operation with visible focus.
- No drag-only, hover-only, gesture-only, or time-limited essential interaction.
- Large enough touch targets and spacing.
- No preselected response that can be submitted accidentally.
- Do not use color, shape, sound, or position as the only cue.
- Allow zoom/reflow without horizontal scrolling for ordinary question content.
- Preserve responses after validation errors.

## High-risk question types

| Type | Risk | Accessible alternative or mitigation |
|---|---|---|
| Slider | value/direction may be unclear; fine motor demands | radio buttons or numeric input; visible current value |
| Matrix | dense reading and focus order | separate questions on small screens; clear row/column headers |
| Drag ranking | keyboard and motor barrier | numbered selects/text ranking with validation |
| Heat map/hotspot | visual-only spatial task | structured region list or image description route |
| Image choice | alt text may reveal/omit meaning | textual equivalent and tested descriptions |
| Timed item | disability and network inequity | remove time limit or offer extension/accommodation |
| CAPTCHA | blocks some disabled users | accessible risk-based alternative and support path |
| Audio/video response | sensory, speech, bandwidth, privacy barriers | text or other equivalent response mode |
| File upload | document access and device limits | alternate submission route and supported formats |

## Plain language and cognition

Use short concrete sentences, familiar words, one instruction at a time, visible examples, consistent scales, predictable navigation, and clear progress. Avoid memory-heavy grids, trick checks, double negatives, and unnecessary time pressure.

## Mobile and low bandwidth

Design for narrow screens, virtual keyboard, intermittent connection, shared devices, and data costs. Avoid wide tables, huge media, fragile session timeouts, and controls that require precision. Offer save/resume only with an appropriate privacy model.

## Inclusion beyond conformance

- Provide language selection before long content.
- Ask names, gender, race/ethnicity, disability, family, and address in ways appropriate to the context and culture.
- Do not require disclosure unrelated to the decision.
- Offer “prefer not to answer” and self-description where meaningful.
- State accommodation/contact options in recruitment.
- Include disabled and otherwise marginalized participants in pretesting; automated accessibility scans are insufficient.

## Testing protocol

Test with keyboard only, screen reader, 200–400% zoom/reflow, mobile portrait, high contrast, reduced motion, slow connection, error states, and representative assistive-technology users when feasible. Verify both completion and exported values.
