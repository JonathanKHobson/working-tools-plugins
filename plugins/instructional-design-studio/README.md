# Instructional Design Studio

Current edition **0.2.2** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Design a lesson, assessment or course path that connects an observable learner task with practice, feedback and evidence of learning. Specialist skills also cover access, AI literacy, production and evaluation.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Create a 25-minute lesson that teaches beginners to check an AI draft against sources.” | Audience, time and source material | Timed lesson with learner practice and feedback |
| “Build a knowledge check from this lesson and show the scoring rationale.” | Approved lesson and target outcome | Questions, answer key, rubric and source checks |
| “Prepare this approved course for recording and LMS handoff.” | Approved course and destination requirements | Production handoff and unresolved delivery checks |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/instructional-design/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Go straight to a specialist for a clear lesson, assessment or handoff. Use instructional-design for broad or mixed work.

| Task / skill | What it produces |
| --- | --- |
| [accessible-learning-design](skills/accessible-learning-design/SKILL.md) | Review or adapt educational materials for access, learner variability, language, assistive technology, and equitable demonstration of the intended skill. |
| [ai-literacy-education](skills/ai-literacy-education/SKILL.md) | Design hands-on AI literacy lessons that teach framing tasks, supplying context, checking outputs, revising, and deciding when human judgment or external verification is needed. |
| [assessment-rubric-design](skills/assessment-rubric-design/SKILL.md) | Design or audit knowledge checks, quizzes, question banks, assignments, performance assessments, rubrics, answer keys, and feedback from learning evidence. Use Survey Studio for experience or opinion measurement. |
| [course-production-handoff](skills/course-production-handoff/SKILL.md) | Prepare an approved course for recording, asset production, review, LMS packaging, maintenance, and delivery verification. |
| [curriculum-backward-design](skills/curriculum-backward-design/SKILL.md) | Design a course, curriculum, syllabus, or learning pathway by aligning outcomes, authentic evidence, prerequisites, practice, and assessments. |
| [edu-role-play](skills/edu-role-play/SKILL.md) | Create interactive learner-vs-AI role-play practice activities with personas, observable objectives, rubrics, debriefs, and optional SCORM/LMS handoff. |
| [instructional-design](skills/instructional-design/SKILL.md) | Guide ADDIE and substantial course-design work toward a concrete learning deliverable and the relevant specialist. Clear lesson or assessment requests can use their specialist directly; simple topic summaries do not need this workflow. |
| [learning-content-storyboarding](skills/learning-content-storyboarding/SKILL.md) | Transform approved source material into lesson scripts, screen-by-screen storyboards, handouts, or instructional explanations while preserving source accuracy. |
| [learning-evaluation](skills/learning-evaluation/SKILL.md) | Design or analyze a course pilot and evaluation using learner performance, retention, transfer, access, and practical improvement evidence. |
| [learning-needs-analysis](skills/learning-needs-analysis/SKILL.md) | Diagnose a learning or performance gap using task, audience, context, and evidence analysis. Use before prescribing training or when an existing course is not solving the stated problem. |
| [learning-experience-designer](skills/learning-experience-designer/SKILL.md) | Apply the complete first-party learner-task, practice, feedback and transfer method to a focused experience. |
| [lesson-experience-design](skills/lesson-experience-design/SKILL.md) | Design a teachable lesson, microlearning unit, playful learning activity, or practice sequence with worked examples, observable learner evidence, feedback, and transfer. Retrieve and adapt assessment activities from the local library when useful. |

## Availability and recovery

Text workflows work with supplied material. The portable edition includes the original fixed-domain `scripts/atlas_library_mcp.py` compatibility launcher. It reads a recipient-owned JSON binding through `--binding` or the current user’s standard studio-tools path; no Atlas server or corpus is bundled. Optional scoped source retrieval can also use a separately installed, user-configured Activities Templates/Atlas capability; [selection rules](references/atlas-library.md) preserve source and rights boundaries. Ordinary text workflows continue from supplied or bundled original references when that optional capability is unavailable.

The activity-search helper uses an explicitly supplied `--library` first, an optional recipient-owned `~/.config/studio-tools/instructional-activity-library.json` binding second, and the bundled 31 original adaptations when no binding exists. A broken binding reports an error instead of silently dropping source context. See [activity archive](skills/lesson-experience-design/references/activity-library.md) for the binding shape and limits.

Methods, examples, maintenance and source/privacy boundaries remain in [the project map](docs/project-map.md) and [verification record](docs/verification.md). Local checkers do not establish learning effectiveness, a working LMS import or publication. Keep course evidence in its owning project.

## Evidence and examples

- [Assessment authoring, blueprints and scoring contract](skills/assessment-rubric-design/references/item-authoring.md)
- [Complete fictional assessment packet](skills/assessment-rubric-design/references/worked-assessment.md)
- [Searchable learning activity archive](skills/lesson-experience-design/references/activity-library.md)
- [Assessment and survey ownership](skills/assessment-rubric-design/references/survey-boundary.md)
- [Reviewed repositories, methods and activity databases](skills/assessment-rubric-design/references/sources.md)
- [Assessment-source security review](docs/assessment-security-review.md)

- [Learning science and design decisions](skills/instructional-design/references/learning-science.md)
- [ADDIE decisions and evidence records](skills/instructional-design/references/addie-decisions.md) (for lifecycle or intervention decisions)
- [September research intake and source limits](skills/instructional-design/references/research-intake-2026-09.md) (for provenance review)
- [Teaching context and reusable defaults](skills/instructional-design/references/personal-grounding.md)
- [AI Workshop Studio v3 planning path](skills/instructional-design/references/ai-workshop-studio-v3-planning.md) (conditional project extension)
- [Worked lesson](skills/lesson-experience-design/references/lesson-patterns.md)
- [Alignment JSON example](skills/curriculum-backward-design/assets/alignment-example.json)
- [Project map](docs/project-map.md)
- [Verification](docs/verification.md)

This public method edition excludes private source locators, transcripts, emails, learner data and full course media. Original workflow and proposed adaptation text remain complete; underlying unknown-rights source summaries and assets are excluded. Attribution does not imply certification, endorsement or a new license for external original content.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public installation and prerequisites

Install this separately versioned package through the [Working Tools repository](https://github.com/JonathanKHobson/working-tools-plugins). Configure the `working-tools` marketplace with the current host's supported flow; in Codex use `codex plugin add instructional-design-studio@working-tools`, then start a fresh task to verify discovery. Use the host's supported removal command to uninstall. Your project, learner and workshop files are separate from the package.

Bring the audience/group, intended observable result, time and approved source material. Text workflows need no account, private Atlas corpus or network service. Original read-only JSON helpers use Python 3.10 or later and the standard library. Visual production needs a separately available document/slide/web or design provider and actual rendered QA. Optional live boards/LMS/media export need your own accounts, permissions and demonstrated provider route. No participant data, credentials, MCP service, background job, tracking or automatic Atlas registration is included. The optional compatibility launcher is source, not a running service.

Example when a provider is missing: "I can prepare the complete lesson/workshop plan from the supplied material. This host currently has no authorized board/LMS editing route, so publishing, participant-role tests and rendered interaction remain unverified. I will provide the run sheet, materials and acceptance checks for the receiving environment." This is an authored expected boundary, not a recorded live execution.

Original scripts in this edition are AGPL-3.0-only. Prose, roles and original teaching/adaptation material are CC BY-SA 4.0 with retained source attribution. Read LICENSE and SOURCE-ATTRIBUTIONS.md. Historical package checks and source observations do not prove learning, a live workshop, public LMS launch, native installation or provider availability. Current static/helper checks are summarized in docs/release-validation.md.

## Standalone method additions in 0.2.0

12 complete skill heads are retained. The added methods are `learning-experience-designer`. Complete references and operative helpers are included; only originating private binding/input records are projected to recipient templates. No automatic installation of providers, hooks or global configuration occurs.

For a first task, supply a fictional learner, one observable outcome and a short source passage. Learning Experience Designer should return a complete practice/feedback/rubric/asset map. Referenced unlicensed notebook, uploader and proxy implementations remain fenced external sources; they are not bundled.
