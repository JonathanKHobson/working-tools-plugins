# Discipline Glossary

Use this file when the user already has a real concept, but is expressing it in UX, marketing, business, or PM vocabulary instead of engineering vocabulary.

## Research and Testing

| Concept | UX / Design | Marketing | PM / Business | Engineering |
| --- | --- | --- | --- | --- |
| Comparing two versions | A/B testing | Split testing | Variant testing | Feature flag / experiment / A/B test |
| Evaluating usability | Usability testing | User research | User validation | QA testing / UAT |
| Expert review of interface | Heuristic evaluation / UX audit |  | Design review | QA audit / review pass |
| Feedback gathering | User interviews | Voice of customer | Stakeholder interviews | Requirements gathering |
| Behavioral measurement | Behavioral analytics | Campaign analytics | Funnel analysis | Event tracking / telemetry / instrumentation |
| Fake flow for learning | Prototype / Wizard of Oz | Landing page test | Validation test | Stub / mock / proof of concept |

## Accessibility and Inclusion

| Concept | UX / Design | PM / Business | Engineering |
| --- | --- | --- | --- |
| Product usable by disabled users | Accessibility / a11y | Accessibility compliance | WCAG compliance / inclusive design / a11y |
| Readable contrast | Color accessibility / contrast ratio |  | WCAG contrast ratio check |
| Screen reader support | Screen reader compatibility |  | ARIA attributes / semantic HTML / AT compatibility |
| Keyboard navigation | Keyboard accessibility |  | Focus management / keyboard trap / tab order |
| Captions and transcripts | Closed captions / transcripts |  | WCAG 1.2 / caption track / VTT |

## Design and Interaction

| Concept | UX / Design | PM / Business | Engineering |
| --- | --- | --- | --- |
| How something signals its function | Affordance / signifier | Discoverability | Interactive state / cursor behavior / ARIA role |
| Low-fidelity version | Prototype / wireframe | Proof of concept | POC / spike |
| Final visual blueprint | High-fidelity mockup / comp | Design spec | Design handoff / redline |
| Reusable UI parts | Design system / component library | Standard templates | Component library / design tokens / UI kit |
| Page or screen structure | Wireframe / layout | Screen layout | Layout spec / responsive grid |
| Flow between screens | User flow / task flow | Journey map | Navigation flow / state machine / routing |
| Interaction details | Interaction design / micro-interaction |  | CSS transition / animation / event handling |
| Information structure | Information architecture | Site structure | Routing / sitemap / navigation hierarchy |

## Performance and Metrics

| Concept | UX / Design | Marketing / Business | Engineering |
| --- | --- | --- | --- |
| How fast the product loads | Page performance | Page speed | Core Web Vitals / LCP / TTFB |
| Desired action completed | Task completion / conversion | Goal completion | Success event / conversion event |
| Users staying active | Engagement / stickiness | Retention | Session depth / retention metric |
| Users dropping out | Drop-off / abandonment | Bounce / churn signal | Exit event / abandonment event |
| Users coming back | Return usage | Retention | DAU / WAU / MAU / retention rate |

## Content and Copy

| Concept | UX / Design | PM / Business | Engineering |
| --- | --- | --- | --- |
| Button text | CTA copy / label | Action label | Button label / link text / aria-label |
| Error wording | Error messaging / microcopy | Error state | Error message / validation string |
| Help or instruction text | Onboarding copy / instructional microcopy | Educational content | Helper text / tooltip text |
| System feedback | Feedback / status messaging | Status update | Toast / snackbar / banner / status message |
| Empty-screen explanation | Empty state copy |  | Empty state / zero state copy |

## Process and Delivery

| Concept | UX / Design | PM / Business | Engineering |
| --- | --- | --- | --- |
| Gradual release | Phased rollout | Staged launch | Feature flag / progressive rollout / canary |
| Pre-launch environment | Staging / testing environment | UAT environment | Staging / QA / sandbox |
| Undoing a bad change |  | Rollback | Revert / rollback / hotfix |
| Breaking systems into pieces | Modular design | Component-based approach | Modularization / microservices / component architecture |
| Behavior rules | Interaction patterns / design principles | Business logic | Application logic / rules engine |
| Review before merge | Design review / critique | Sign-off | Code review / PR review |

## Fast Translation Rules

- If the user names a recognized discipline term, translate it directly and include the engineering search term.
- If multiple engineering terms are plausible, prefer the one that best matches the delivery layer: frontend component, API concept, analytics event, or rollout mechanism.
- If the user is really asking for implementation structure rather than vocabulary, switch to `Mode 4` and load `idea-to-spec.md`.
