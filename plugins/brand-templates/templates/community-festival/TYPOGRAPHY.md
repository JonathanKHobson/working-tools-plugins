# Common Sun · typography

Anton is the source's display family; Arimo is the source's body family. The source CSS and usage observations are summarized in [evidence.json](evidence.json). Packaged files and redistribution terms are enumerated in [assets/manifest.json](assets/manifest.json); both families include SIL Open Font License text in this kit. Keep those notices with the fonts when redistributing them.

| Role | Family | Use |
| --- | --- | --- |
| Display | Anton | Short, high-priority headings, event title, date emphasis, and brief wayfinding labels. Prefer the source's uppercase treatment where it fits. |
| Body | Arimo | Schedule details, venue/access information, longer copy, controls, and explanatory text. Use regular and bold weights as needed. |

Keep headings brief enough to avoid crowding the date line. Give times, session titles, and venues separate typographic cues. Never shrink access or schedule details merely to force a headline to fit. In documents or slides, map the two families to native heading/body styles so the hierarchy remains editable and accessible.

If either family is unavailable, use a locally available condensed sans for display and a neutral sans for body, then test line breaks, page count, and hierarchy against the original. Record the substitution. A CSS family declaration or included font file does not prove that the target application loaded that font; inspect the rendered/exported artifact. Production logo lockups use outlined Anton lettering and do not require the font to render; see [LOGO.md](LOGO.md).
