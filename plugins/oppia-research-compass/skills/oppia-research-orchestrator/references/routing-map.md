# Oppia Research Routing Map

## Priority Order

1. Search and retrieve Oppia evidence.
2. Answer from evidence when it is decision-sufficient.
3. Select one method skill for a specific remaining gap.
4. Use explicit external research only when internal and Drive sources cannot
   answer the gap.

After selecting a lane, apply `research-quality-gates.md`. Method choice follows
the evidence needed, not the stakeholder's preferred deliverable or a universal
participant-count rule.

## Lane Matrix

| Request signal | Primary lane | Required first action | Typical deliverable |
| --- | --- | --- | --- |
| prior findings, evidence, studies, interviews | MCP / `oppia-research-compass` | Search Oppia corpus | Evidence brief |
| vague request, reported problem, proposed solution, question audit or backlog | `oppia-research-question-design` | Search prior evidence; separate signal, problem, decision, and gap | Oppia RQ framing card |
| interview guide, discussion guide, discovery interview | `oppia-interview-study-design` | Check existing interview evidence | Moderation guide |
| task test, prototype test, observed flow | `oppia-usability-testing` | Check prior findings and CUJ | Test plan and script |
| alternatives, comparable products, feature comparison | `oppia-competitive-analysis` | Define Oppia decision and comparison set | Evidence matrix |
| Reddit, forums, public community discourse | `oppia-netnography` | Check corpus and ethics boundary | Provisional netnography plan or synthesis |
| identify, validate, revise personas | `oppia-persona-research` | Browse interviews/persona records | Evidence-confidence scorecard |
| expert review, heuristic scorecard, severity | `oppia-heuristic-evaluation` | Define persona, CUJ, device, and scope | HE findings packet |
| critical user journey, journey health, goal path | `oppia-cuj-research` | Retrieve relevant evidence and current CUJ | CUJ proposal or gap audit |

## Multi-Lane Rules

- Question design may precede any new study, but it is not a required extra
  artifact when the decision question is already clear.
- Question framing owns problem definition, question layers, learning
  objectives, evidence alignment, and prioritization. The selected method skill
  owns the later study design or instrument.
- Persona or CUJ work may use interview, usability, heuristic, competitive, or
  netnography evidence. The persona/CUJ skill owns synthesis; the method skill
  owns data collection design.
- Heuristic evaluation is expert inspection, not a replacement for observed
  usability when behavior is the uncertainty.
- Competitive analysis describes comparable patterns; it does not establish
  what Oppia users need.
- Netnography provides contextual signals; it does not make a public community
  representative of Oppia's learner population.
- A consequential contradiction routes back through evidence audit before a
  new study is designed.
- Accessibility, language, culture, infrastructure, age, and power can change
  method validity; they are not optional appendix topics.
- AI may support permitted, reversible, source-traceable work, but the named
  researcher remains accountable for interpretation and decisions.

## Wrong-Lane Examples

- "What have learners said about navigation?" is corpus retrieval, not a new
  interview plan.
- "Can five volunteers review this flow tomorrow?" is heuristic evaluation,
  not usability testing, unless participants will attempt tasks.
- "Rewrite the entire CUJ document" is not authorized by a request to research
  one journey; produce a bounded proposal or diff.
- "Find what Reddit says" is not a persona update until evidence is sampled,
  analyzed, triangulated, and confidence-labeled.
