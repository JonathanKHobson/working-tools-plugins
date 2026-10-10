# Adoption Map

Reviewed sources:

- `minicoursegenerator/skills-for-course-creators`
- `minicoursegenerator/edu-role-play`
- `minicoursegenerator/vimeo-dot-net`
- `minicoursegenerator/ai-hallucination-checker`
- `minicoursegenerator/edu-role-play-proxy`

Adopted locally:

- Course asset routing by outcome: create, research, convert, visualize,
  practice, analyze, publish.
- Role-play practice as a first-class learning asset.
- Rubric and observable-objective discipline.
- Shareables as a course packet, lesson explainer, or progressive-disclosure
  review artifact.
- Source-consistency checks for generated learning content.

Fenced:

- Vimeo API wrapper: old .NET library, credentialed upload/account operations,
  no local install. Use only as a reminder that video publishing needs OAuth,
  upload permission, metadata review, and official current API docs.
- Hallucination checker notebook: no license and semantic-similarity-only
  approach. Recreated as a source-consistency warning, not as a copied tool.
- Role-play proxy: optional deployment pattern only; no vendored code without
  a license and no secret handling outside the provider dashboard.

