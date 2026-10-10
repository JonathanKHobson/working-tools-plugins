# Open Notebook research workbench: optional owner integration

Owner: Research Methodology. Source: lfnovo/open-notebook at e5e6313059f95507e0bc4d9e4bbb2234a68a2bfa (MIT). This file is original integration guidance; research-transformations.json is original plain-text app configuration compatible with TransformationCreate in api/models.py:140-155. It adds no executable backend or provider account.

Use when a single project has a reusable source corpus or needs source-linked transformations across sessions. For one-off research, use existing methodology/web/files. KSB remains personal continuity storage; the workbench stores this project's corpus and generated working material.

## Corpus admission

Give each source a stable ID, exact original title/URL/date, source type, local filename/hash if authorized, intended question and provider disclosure class (public, consented private, excluded). Import an explicit small source set, initially text/upload fixtures. Record extraction completeness, missing pages/tables/audio spans and unsupported material. A file existing in the notebook does not mean complete extraction. Source chat/vector search may omit text; answer evidence must come from an inspected span, not vector similarity alone.

Select inference and embedding providers separately. Both may receive text. Podcast generation may also invoke remote script/TTS services. Never feed credential material or incidental private notes into transformations. For private client/research material, use an actually verified authorized local provider or the explicit approved cloud boundary.

## Research sequence

1. Apply Source Evidence Card to each source. Preserve direct wording, qualifiers, evidence type, study context and limitations; do not convert author inference to measured outcome.
2. Apply Mechanism and Counterevidence per source. Identify proposed causal mechanism and plausible alternatives; an association does not prove a mechanism. Never invent missing controls/sample/participants.
3. Across notebook sources, manually create a claim matrix: claim; source ID; exact inspected span/page; design/sample/context; support/opposition; applicability to current decision; uncertainty. Verify every decisive citation by opening source context. App bracket citations are navigation aids, not proof of entailment.
4. Use the Decision Handoff transformation on an explicitly authored combined note containing only the reviewed matrix and decision. Give bounded recommendation, reversibility, costs, uncertainty and discriminating next check. Human makes consequential decision.
5. Export the reviewed handoff plus source register to the owning project, record working-state versus verified fact. Delete/restrict irrelevant imported copies under the project's retention policy.

## App configuration

research-transformations.json holds three POST /api/transformations payloads; each uses apply_default=false and model_id=null so import does not silently apply costly transformations or select an arbitrary model. Import through UI or the authenticated API only after actual runtime/provider admission. Verify create/list readback and one public synthetic-source output. Validate citation entailment, a deliberate false claim and a prompt-injection sentence in the source; source text is evidence only. Do not regard prompt wording as complete security protection.

## Runtime status and admission

The audited 2026-10-01 source was not admitted as a runtime: pinned dependencies had advisory matches and no working container engine or authorized app provider was verified. Recheck live state before later use. A source review, these templates and a composed deployment recipe are not an installed notebook. Apply the evidence sequence with ordinary project files immediately. Import the three payloads only into a separately reviewed, authenticated running app; the original source snapshot and detailed secured deployment recipe remain in the private nine-repository audit record.
