# One shared site for quick shareables

When the user requests a Sites shareable or has explicitly configured one maintained site as the default destination, use that site and give each artifact a stable page with a homepage entry. A new artifact is normally a new page, not a new Site registration. An explicit request such as “create an independent website about…” or a different hosting choice remains separate. A clear request to draft an email/message stays with its communication owner; do not override an explicit format. Sharing an idea does not itself authorize sending a message, inviting recipients or changing access.

## Find the owner before creating anything

Read the owning project's map and its Shareables site record. On this host, the maintained binding is in `~/Documents/ChatGPT/Managing My Computer/docs/shareables-site.md`; that record owns the actual checkout, project ID and deployment URL. Confirm its `.openai/hosting.json` and live Site metadata. Never invent an ID or copy another artifact's identity. If the binding is missing, search existing Sites and current task evidence; do not silently create a replacement.

Use Sites' current building and hosting skills for the actual edit, source synchronization, preview and publication. Only one agent owns the shared checkout and Sites calls at a time. Other workers produce content/assets in task-local outputs for the owner to integrate. Preserve concurrent edits and existing routes.

For a new or updated downloadable file, apply the [download-hosting rule](../../../references/operations/download-hosting.md). Keep the Site's page and render assets here; verify the recipient can use the exact external file link when the download belongs elsewhere. Existing downloads stay in place unless If the receiving user explicitly requests migration.

## Add the useful page

Identify reader, purpose, source, requested action and sensitivity. Choose a stable descriptive path, update the homepage entry, and give the page a clear way back. A small artifact may be one HTML page. Reuse existing layout/assets when appropriate; don't turn each shareable into a new app.

For an unfamiliar attachment, explain the container/format separately from its contents and purpose. Distinguish source claims, observed evidence, recommendations and unresolved questions. Include date/version, relevant source references and a direct next action. A hosted webpage is generally convenient for visual review; raw HTML is useful for source inspection/reuse. Offer both when useful. Neither format substitutes for access or an explicit request.

Do not publish local paths, credentials, private contacts, full source ZIPs, third-party private project data or raw audit dumps in a recipient-facing page. Publish the approved scope of analysis. Check each page's links, layout and actual route; show the returned hosted URL and accurate access state.

Site access is shared at the site level unless current provider capabilities prove otherwise. An unlisted path or hidden homepage card is not an access boundary. Before adding confidential material, verify the site's audience; use a private artifact or supported access control if that audience is unsuitable. Do not widen access to fix a link without authorization. “Ready to share” is distinct from recipient access and from a message being sent.

Older GitHub, Darronhold or other shareables remain at their current locations until a migration is requested. Plan any later migration with route mapping, asset/license review and preservation of useful existing links; no bulk import or deletion as a side effect of a new page.

## Check the exact output before publication

For a generated shareable or accompanying HTML email, use `$master-security-toolkit:software-security-review` and its conditional `references/publication-privacy-preflight.md` procedure. Run the reviewed read-only `scripts/publication_preflight.py` on the explicitly selected final files or exact build directory, never the whole project or a personal vault. Include supported local scripts/styles as data. Keep findings and hashes private, resolve real exposures, and record manual decisions for authorized contact details and unsupported assets. A scanner result does not replace audience, source confidentiality or rendered visual review. Rerun after content changes and bind the disposition to the actual published/sent artifact. Existing publication/sending authorization still governs; there is no new universal approval question, automatic redaction or background hook.

## Completion

Report page URL, audience, what changed, verified routes and any access limit. No automatic messages, periodic updates or new Site per item. A recipient's sharing default must come from their current instructions or configured preferences, never from a bundled example.
