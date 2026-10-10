# Bundled methods and publisher-installed extensions

The complete locally authored [manuscript craft](../../skills/academic-writing/references/manuscript-craft.md) and [evidence/tool audit](../../skills/academic-writing/references/evidence-and-tools.md) are the academic-writing fallback. The complete [study planning method](../../skills/research-methodology/references/study-planning.md), [guides](../../skills/research-methodology/references/study-planning-guides.md), [records and synthetic example](../../skills/research-methodology/references/study-planning-records-and-example.md), [qualitative analysis](../../skills/research-methodology/references/qualitative-analysis.md), and [document-to-method conversion](../../skills/research-handoff/references/document-to-method.md) are bundled. They remain usable without a publisher plugin. They do not impersonate the following provider-specific procedures.

| Exact optional provider route | Publisher-installed capability | When to use | If absent |
| --- | --- | --- | --- |
| `aihumanizer:academic-writing` | Natural academic prose editing | User requests this provider or its distinct voice technique | Use bundled manuscript craft; do not claim provider pass. |
| `aihumanizer:essay-humanizer` | Essay-specific style review | Essay polish within the assignment's assistance limits | Use bundled manuscript craft and coursework checks. |
| `research-writing-guardrails:compag-elsevier-paper-editing` | COMPAG/Elsevier specific manuscript editing | Target journal and provider are available; verify current author instructions | Use bundled evidence/tool audit and current journal instructions; no provider-specific claim. |
| `research-writing-guardrails:research-problem-mechanism-evidence` | Named research argument diagnostic | A technical paper needs this provider's full procedure | Use bundled evidence/tool audit, with its own scope. |
| `uiuxdesigner:personas-journey-maps` | Publisher persona/journey method | Persona or journey artifact needs that method | Keep source-grounded study findings; name unavailable artifact method. |
| `uiuxdesigner:ux-research-plan` | Publisher UX research planning method | User selects that provider | Use bundled study planning method. |
| `uiuxdesigner:usability-testing` | Publisher usability procedure | User selects that provider | Use bundled study planning method and guide. |

Install these plugins from their official provider distribution on the recipient host; their installation and authentication are separate from this package. Codex discovery can select the names above if the plugin is installed. Claude installations require that the same publisher skill be installed separately in Claude; this package cannot transfer a Codex-installed plugin to Claude. If a route is missing, continue only with the stated bundled method and label any provider-specific operation unrun. There is no hidden copy of a publisher method here.

## Preserved local source procedures

- [Complete original current-social-research instruction](local/current-social-research/SKILL.original.md), [source-plan reference](local/current-social-research/references/last30days-adoption.md), and [planner script](local/current-social-research/scripts/current_social_plan.py). These are source preservation; the active skill chooses the task-matching current method.
- [Local interview original](local/study-planning/oppia-interview-study-design.SKILL.original.md), [local usability original](local/study-planning/oppia-usability-testing.SKILL.original.md), [quality gates](local/study-planning/research-quality-gates.original.md), [external method review](local/study-planning/external-source-review-ux-research-skill-v1.0.0.original.md), and [attribution/dispositions](../../skills/research-methodology/references/study-planning-provenance.md). These archives are inactive; no Oppia corpus is included.
