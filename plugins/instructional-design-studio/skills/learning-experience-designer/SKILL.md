---
name: learning-experience-designer
description: Design practical learning experiences, mini-courses, workshops, lessons, facilitator guides, learner worksheets, role-play practice, assessments, rubrics, and course production plans. Use when the user asks to make a course, training, lesson, curriculum, worksheet, workshop, learning path, mini-course, or education asset.
---

# Learning Experience Designer

Turn knowledge into a teachable experience with a clear learner, objective,
practice loop, evidence, assessment, and delivery format.

This skill folds in the useful course-creator mapping from
`minicoursegenerator/skills-for-course-creators`, the role-play workflow from
`edu-role-play`, and local coordination with documents, slides, Shareables,
communication, and visual asset skills.

## Use This Skill When

- The user wants a mini-course, lesson, workshop, module, facilitator guide,
  worksheet, quiz, or learner handout.
- A transcript, article, notes dump, talk, project, or process should become
  training material.
- A learner needs practice, feedback, or assessment, not just explanation.
- The work should route to docs, slides, role-play, Shareables, video/audio, or
  an LMS-ready artifact.

## First Move

Classify the learning job:

1. Course or learning path
2. Single lesson or workshop
3. Worksheet or handout
4. Slide deck or HTML presentation
5. Role-play / simulation practice
6. Assessment, rubric, quiz, or reflection
7. Source conversion from transcript, video, PDF, notes, or docs
8. Course operations plan, asset map, or publishing checklist

Then identify:

- learner and prior knowledge
- job-to-be-learned
- observable learning outcomes
- evidence/source material
- practice activity
- assessment or feedback loop
- delivery surface

Ask at most one clarifying question if one of those would change the artifact.

## Design Rules

- Start with observable outcomes. Avoid "understand" as the final learning goal.
- Build for transfer: what the learner can do later in a real context.
- Use the smallest useful scaffold: example, worked example, faded example,
  practice prompt, checklist, rubric, reflection, or role-play.
- Pair each concept with one learner action.
- Put practice before polish when the goal is skill-building.
- Separate source truth from instructor interpretation.
- Mark missing facts instead of inventing examples, data, outcomes, or policies.
- Use plain language unless the learner is already expected to know the domain
  vocabulary.
- Keep accessibility and cognitive load visible: reading level, chunking,
  alt text, pacing, and non-text alternatives.

## Asset Routing

Route the output to the narrowest useful local skill or tool:

- `edu-role-play`: persona practice, conversation drills, simulation scoring.
- `html-presentation-builder`: browser-based lessons, slide decks, technical
  walkthroughs, data-rich teaching decks.
- `communication-story-crafter`: explanations, hooks, lesson narrative,
  stakeholder or student-facing copy.
- `visual-asset-integration`: images, screenshots, diagrams, source labels,
  alt text, crop/placement, and QA.
- `documents` or local document skills: handouts, facilitator guides, DOCX/PDF.
- `spreadsheets` or data skills: trackers, learner data, rubrics, schedule maps.
- Shareables MCP: public-safe field guides, course explainers, packets,
  progressive-disclosure pages, and review artifacts.

## Course Asset Map

For non-trivial work, produce or update this map:

```markdown
## Learning Asset Map
- Learner:
- Outcome:
- Source material:
- Delivery surface:

| Asset | Learner job | Format | Source truth | Practice/feedback | Status |
| --- | --- | --- | --- | --- | --- |
```

## Learning Blueprint

Use this shape for lessons and modules:

```markdown
## Learning Blueprint
- Audience:
- Outcome:
- Prerequisites:
- Time:
- Evidence/source base:

## Sequence
1. Hook or relevance:
2. Explain:
3. Worked example:
4. Practice:
5. Feedback:
6. Transfer task:
7. Assessment:

## Rubric
| Criterion | Observable evidence | Weight | Full-credit signal |
| --- | --- | --- | --- |

## Delivery Notes
- Accessibility:
- Visual assets:
- Instructor notes:
- Open questions:
```

## Shareables Pattern

When creating a Shareables artifact for a learning asset:

- Use `docs` for how-to guides and technical setup.
- Use `packet` for course overview plus separate instructor/learner pages.
- Use `reel` for short screen-by-screen learning summaries.
- Use `storyboard` for conceptual explainers and journey maps.
- Include progressive disclosure: overview first, then method, then references,
  then technical appendix.
- Keep learner-facing content distinct from authoring/deployment notes.

## Runtime And Security Boundaries

- Do not install course tools, scrapers, LMS integrations, video uploaders, or
  API clients unless a separate security review approves the exact runtime.
- Do not upload student/learner data, private transcripts, assessment results,
  or client materials to external services without explicit approval.
- Do not imply SCORM/LMS compatibility unless an actual package was produced or
  the output clearly says it is a plan.

## Output Contract

Return the artifact first, then a short build note:

```markdown
## Learning Output
[artifact]

## Build Note
- Outcome coverage:
- Practice/feedback:
- Source limits:
- Next production step:
```

