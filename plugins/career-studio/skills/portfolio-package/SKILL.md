---
name: portfolio-package
description: Assemble or refresh coordinated portfolio websites, resumes, and slide decks from local work samples, with shared evidence and consistent requested role variants, such as UX Design and UX Research. Use for a portfolio package or cross-format assembly request; use the format-specific skill for an isolated resume rewrite or case-study edit.
---

# Portfolio package assembly

Turn existing work samples into a coherent, reviewable portfolio package. Finish the requested artifacts using one shared set of verified facts and assets.

## Establish the package

Read the current request and applicable workspace instructions. Identify the target reader, role, requested artifacts, source roots, output location, formats, and sharing destination. Resolve these from supplied context first; ask only for a missing decision that materially changes the work. Continue independent local preparation while an essential answer is pending.

A full package may include role-specific sites, resumes and decks. Build only the requested sets, in the user's priority order, and finish one coherent set before adapting it. For source locations use the existing private workspace or [private workspace binding](../../references/private-workspace.md); the plugin carries no candidate profile or default portfolio directory. Historical projects do not establish current claims or publication authorization.

State the verification path at the start: trace claims to sources, compare all variants, open the actual exports, visually inspect rendered surfaces, and verify live URLs only if publication is requested.

For evidence-led web delivery, role-specific reuse, and a bounded release check,
read [evidence-led-delivery.md](references/evidence-led-delivery.md). Apply it to
the role sets actually requested, including adjacent applied-AI or analyst roles;
historical paired-package examples do not limit current scope.

## 1. Resolve and inspect the sources

- Resolve source roots from the current user and private project. Distinct mounted paths are not interchangeable; verify the owning folder before editing.
- Start with a bounded inventory using `rg --files` or an equivalent listing. Inspect existing HTML, case studies, screenshots, assets, resumes, slide templates, and decks with format-appropriate readers. A filename or Finder listing proves presence, not the claims inside it. Extract PDF, DOCX, and PPTX content; do not read binary documents as plain text.
- Compare apparent duplicates by relevant content and, when useful, hashes. File modification times and names such as `v2` do not establish factual authority. Prefer newer reviewed evidence over old resumes; use archives as leads until reviewed. Preserve originals and record unresolved conflicts.
- Treat network folders and Google Drive as evidence sources. Copy only selected inputs into the working package when needed; the finished package should not depend on a specific mounted device or private Drive session. If an extra source is unavailable, continue with accessible evidence and name only the resulting gap.
- Consult `work-management:project-structure` if that installed skill is discovered before expanding project files; otherwise follow the owning project map and this package's [project map](../../docs/project-map.md). Reuse a suitable existing site structure and template. Keep shared content, selected assets, presentation code, and exports separate, and update `docs/project-map.md` for a growing implementation. Do not create a new framework, MCP, or portfolio management system just to assemble the package.

## 2. Build one compact evidence map

Keep a private working note or table that all requested role variants and formats use. Extend an existing evidence map if it already serves this purpose.

| Field | Record |
| --- | --- |
| Evidence ID and project | Stable local ID; preserve existing source IDs |
| Supported fact | Role, contribution, date, method, decision, outcome, or metric |
| Source and locator | Exact file plus page, slide, section, or screenshot |
| Review status | Reviewed current evidence, archival lead, adjacent evidence, or unresolved |
| Asset status | Real work, illustrative, cropped, redacted, or reconstructed |
| Sharing status | Approved for public use, private, or permission unknown |
| Reuse | Design/research case, resume bullet, and slide where used |

Never invent metrics, titles, dates, methods, clients, team ownership, tools, or outcomes. Label adjacent evidence as adjacent. Use `[MISSING INFO: ...]` in private drafts for missing facts. Before a share-ready export, resolve the gap, omit the unsupported claim, or use truthful limited wording; do not hide uncertainty with polished language.

If job-application-compass is available and relevant, use its reviewed profile and evidence search to corroborate facts. Preserve its source tiers and personal-write confirmation rules. Assembly does not authorize profile changes. An absent connector should not block work supported by local files.

## 3. Shape the cases before laying out the formats

Choose the strongest supported cases for the intended reader, usually a small set rather than the entire archive. For each, establish the problem, the candidate's actual role, constraints, work performed, artifacts, decisions influenced, and evidenced outcome or learning. Put a concrete artifact near the claim it supports.

For example, if the requested package pairs UX Design and UX Research roles, use the following emphases; other roles follow the same evidence rule.

| Variant | Emphasis | Facts that must stay consistent |
| --- | --- | --- |
| UX Design | Flows, interface decisions, iterations, constraints, and implementation or handoff evidence | Employment titles, dates, ownership, methods actually used, and outcomes |
| UX Research | Research questions, methods, synthesis, findings, recommendations, and decisions informed | The same underlying project facts and limitations |

Mirroring changes the selection, order, captions, and emphasis. It does not turn a design review into a study, invent participants, or rewrite employment history to match the target role.

Use this plugin's `portfolio` skill for case selection and claim integrity and `resume` for resume structure. If `writing-quality-studio:communication-crafter` is actually discovered, use it for a clear narrative; otherwise review the narrative directly for plain language, proof near claims, and a clear next step. For recruiters, make role and contribution easy to scan; for freelance or contract readers, connect the work to the problem solved and evidence of reliable delivery. Choose one primary audience when priorities compete.

## 4. Assemble a complete set, then adapt it

Reuse the evidence map and case narratives across formats. For a paired package, finish one coherent role set before adapting the second. A first-set checkpoint is useful progress, but it does not complete a request for both sets.

- **Website:** Provide positioning, selected cases with real work images and captions, clear role/contribution, and access to the correct resume, deck, and contact route. Preserve useful existing implementation and visual language. Keep content and assets shared where practical, with role-specific presentation. Select frontend or site tooling that fits the existing project and requested host.
- **Resume:** Produce an editable source and a readable, selectable-text PDF when formats are unspecified. Use the same verified titles, dates, project names, and outcomes as the site. Adapt summary and bullet emphasis to the role. Verify reading order and links in the exported file.
- **Slide deck:** Build a concise spoken narrative around the same cases, using actual screenshots or exports at readable scale. Prefer an existing editable slide format/template; provide an editable deck and a PDF for review when formats are unspecified. Keep proof, ownership, and outcome visible; place supporting detail in notes or an appendix when useful.

Use the installed document, slide, PDF, or frontend workflow only when needed for that artifact. In Codex desktop, load bundled workspace dependencies for document and deck work when that helper is available; in other hosts use their supported document and slide tools and inspect the actual exports. Historical plugin selections are capability hints, not a required toolchain. Do not add video, outreach, dashboards, or extra publishing destinations unless requested.

Real screenshots and work exports are evidence; generated decoration is illustration. Inspect and caption proof assets before placement. Preserve originals when cropping or redacting. Do not create fake product screens, testimonials, or logos to fill gaps.

## 5. Verify the actual package

Apply these checks to the requested artifacts and variants, against their final files after substantive changes:

1. **Evidence and consistency:** Trace every material claim and displayed proof asset to the evidence map. Compare identity, employment titles, dates, ownership, outcomes, project names, and contact details across the requested variants, resumes, decks, and download links. Check that each site links to its own intended files.
2. **Functional and export checks:** Open each requested site and the actual exported resumes and decks. Test navigation, downloads, keyboard access, contact links, and variant switching if present. Check missing assets and errors. Verify PDF text extraction and slide/page counts, and inspect speaker notes and document metadata for unintended private content.
3. **Visual QA:** Render every resume page and slide; inspect each distinct site layout on desktop and mobile, including a short-height desktop viewport. Check readable type, clipping, overlap, image crops, contrast, focus, and download placement. A successful export command is not visual QA.
4. **Grounded review:** Before visual claims or fixes, create 3–8 representative anchors: `ID | source and viewport/page | region or normalized coordinates | selector/component if available | observation | intended action | verification`. Refer to anchors in findings and recheck changed anchors. Keep any unreviewed surfaces explicit.
5. **Final craft and communication:** After usability checks, use `ux-design-toolkit:design-studio` and `writing-quality-studio:communication-crafter` only when those installed skills are actually discovered. Otherwise perform the first-party anchored visual review above and a direct plain-language pass for reader fit, proof near claims, and clear next steps; do not claim a provider review. Real case evidence should lead the visual design. Remove generic filler and unsupported superlatives.

When the local `codex_artifact_quality_gate.py` helper is available, mark `visual_qa`, `design_taste`, and `communication_review` with the reviewer and concrete evidence after review. Skip only genuinely inapplicable checks with a reason. Otherwise record the same checks in the working QA note. A mark records review; it does not perform it.

If browser automation was used on the recipient's computer, close automation-owned browser sessions and verify normal browser handoff before signoff. Do not close unrelated user sessions.

## 6. Deliver or publish within the requested scope

Local assembly and public publication are separate states. Complete authorized local work before requesting any missing publication decision. If the user already authorized the exact public scope and destination, proceed after verification without asking again.

A past hosting choice is not standing permission to publish. For a current GitHub request, verify the actual repository, target branch/path, hosting configuration, and public-safe file set. Follow the available hosting workflow and check the deployed URLs, assets, navigation, and downloads. Use deployment evidence, not a staged commit or a proposed URL, to report publication.

Publish only the reviewed output set. Keep raw evidence, archives, private source paths, hidden tool folders, client-sensitive material, and unapproved assets out of it. Resolve sharing uncertainty for affected material while continuing the rest of the package.

Close with direct links and a compact status for every requested role set: site, resume, and deck; local verified or published verified; checks completed; and any remaining factual or permission gap. Do not call a plan, inventory, partial package, or uninspected export finished. Once the requested package passes, stop adding features.

For document, PDF, slide, website, visual, and publishing work, use the current [provider boundary](../../references/providers.md) only when that output is requested.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Producer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
