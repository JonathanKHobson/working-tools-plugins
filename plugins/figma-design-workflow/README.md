# Figma Design Workflow

Turn a design reference or existing screen into an editable Figma artifact, then verify its visible result and structure. Bring the Figma file or target frame, the change you want, approved visual references, and any must-keep content. The workflow can also prepare a reference, transfer selected Stitch screens, or build a FigJam workshop board.

Try a first request:

- “Import these selected Stitch screens into this Figma file and confirm the text and layout are editable.” Result: verified frames and a clear account of any transfer gaps.
- “Update this Figma screen to match the approved reference while keeping these labels.” Result: an edited frame and visual QA against the source.
- “Build a FigJam workshop board for this agenda with staged reveal.” Result: an editable board with the relevant controls checked in the actual editor.

For a capabilities/getting-started question or broad Figma operation, start with [Figma Operator](skills/figma-ui-operator/SKILL.md). For a defined transfer, reference, or review, choose the matching skill in the [project map](docs/project-map.md). This README is a human guide; it is not automatically loaded into an AI task.

| Task | Skill |
| --- | --- |
| Consult available Mac design partners | [Mac Design Partners](skills/kyle-mac-design-partners/SKILL.md) |
| Prepare source-faithful Figma-to-Stitch iterations | [Figma-to-Stitch](skills/figma-to-stitch-design-iteration/SKILL.md) |
| Edit in Figma or build an editable FigJam board | [Figma Operator](skills/figma-ui-operator/SKILL.md) |
| Move selected Stitch screens into editable Figma layers | [Stitch to Figma](skills/stitch-figma-handoff/SKILL.md) |
| Prepare one visual north star | [Design Reference Prep](skills/design-reference-prep/SKILL.md) |
| Review the rendered design before handoff | [Design Visual QA](skills/design-visual-qa/SKILL.md) |

Use the step that serves the current deliverable. Claude/imagegen → Stitch → Figma is available when visual exploration helps; routine edits can go straight to Figma.

The plugin teaches workflows. Computer Use, built-in imagegen, Figma tools, and signed-in Claude/Stitch apps remain external runtime capabilities. Installing this bundle does not enable OS permissions, buy credits, or publish designs.

For automatic discovery, start a new Codex task after installation. Existing tasks can read the exact skill path immediately. See docs/project-map.md and docs/validation.md for structure and tested scope.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Installation and prerequisites

Install the separately versioned `figma-design-workflow` package from the [Working Tools plugin repository](https://github.com/JonathanKHobson/working-tools-plugins). The portable root manifest and Codex/Claude compatibility manifests expose the same four method heads. In Codex, after the `working-tools` marketplace is configured, use `codex plugin add figma-design-workflow@working-tools`, then start a fresh task to check discovery. Use the host's supported plugin removal command to uninstall; removal does not delete your Figma documents.

For editor work you need your own Figma account, permission to the intended file, and an available authorized Figma connector or Computer Use route. Computer Use needs the host's browser/app permissions. Optional Stitch transfer requires your own accessible Stitch session and a demonstrated editable export/import route. Reference generation requires a separately available imagegen or Claude capability. Accounts, API keys, provider apps, paid credits, native role registration, MCP servers and OS permission grants are not included. The packaged structural checker uses Python 3 and the standard library; Python is not needed merely to read these methods.

If a provider or control route is missing, record the unmet prerequisite and prepare the brief, source anchors and intended checks from the supplied material. Do not claim a canvas edit, editable import, image generation or rendered QA. The [missing-provider scenario](docs/missing-provider-example.md) shows the expected boundary. Setup guidance must follow the actual current host, rather than a machine path in a historical receipt.

## Rights and verification

Original workflow text, fixtures, role contract and helper are released under the [MIT license](LICENSE). [Source attributions](SOURCE-ATTRIBUTIONS.md) retain the original primary-source register, user-supplied ZIP lineage and adaptation boundaries. No Figma, Google Stitch, Claude or OpenAI provider code, tutorial transcript, vendor screenshot or font is bundled. Names identify interoperability and do not imply endorsement.

Run `python3 skills/figma-ui-operator/scripts/validate_skill.py --json` from the package root. See [current export validation](docs/release-validation.md) for exact checks and limits; [historical validation](docs/validation.md) remains explicitly dated. A static package pass does not prove receiving-host installation or live Figma, FigJam, Stitch, Claude, imagegen, multiplayer, accessibility or participant outcomes.

## Version 0.2.0 complete design-partner methods

Two complete four-file original workflows are added. Private author-host observations and client-specific iteration evidence are replaced only in their exact support units by explicit receiving-host/synthetic examples. All selection, brief, account/usage verification, scratch-workspace, export, attachment reconciliation, authority, Change/Keep/Defer and visual-check procedures remain. The skill names retain source identities; they assert no account access or historical user authorization for a recipient. A synthetic draft/source audit does not prove provider generation, rendered output or editable Figma import.
