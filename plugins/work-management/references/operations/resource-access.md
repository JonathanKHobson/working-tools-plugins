# Find and use external resources on demand

Use this route when a task names a site or a specific design, asset, component, prompt or travel question would benefit from one. The [resource directory](resource-directory.json) contains 74 resource records with identity and access findings as of 2026-10-22. It is a finding aid, not a collection to browse wholesale, a grant to reuse assets, or a claim that every site has an API. Resolve this plugin's installed root through skill discovery; do not copy paths from another host.

## Find a relevant record offline

`resource_access.py` reads the bundled directory without network access. List a domain, search words, or inspect the full record:

```sh
python3 /installed/work-management/scripts/resource_access.py list --owner ux-design-toolkit
python3 /installed/work-management/scripts/resource_access.py list --category motion-inspiration
python3 /installed/work-management/scripts/resource_access.py search 'motion'
python3 /installed/work-management/scripts/resource_access.py show designmd-app
```

Use the selected Studio's method for the actual work. Prefer a connected official tool or documented official API when it covers the task. Next, use an operation that is listed and tested for the exact purpose. Use the browser for visual inspection or an unsupported request, subject to the user's access and the site's terms. A record's `api_anything.status` and `operations` describe specific reviewed capabilities, not general site coverage. Confirm the operation and its inputs before a call. A browser fallback or a recipe file does not mean an operation is currently working.

For galleries, select a few relevant examples and record the exact item, creator, visible mechanism and intended adaptation. Carry relationships such as hierarchy or transition purpose into original work under the project's identity; do not clone the page or treat public visibility as an asset license. Check current attribution, commercial use, redistribution and dependency terms for selected fonts, images, templates and code. An unresolved identity stays unresolved until its exact URL or publisher is confirmed. Do not replace it with a similarly named service.

## Install a reviewed API Anything recipe when needed

The bundled [recipe directory](api-anything-recipes/) contains a small set of audited site specs and notes. Installing one is an explicit local file copy into a recipient-selected API Anything state directory outside the plugin. It does not install the API Anything runtime, contact the site, import a browser profile or activate an MCP connection. Supply the same state path chosen for [API Anything setup](api-anything.md):

```sh
python3 /installed/work-management/scripts/resource_access.py install-api designmd-app \
  --state /chosen/private/api-anything-state
```

The helper checks the reviewed SHA-256 manifest and admits only specs whose operations are marked read-only GET. It refuses missing or changed recipes, symlink/traversal destinations and differing existing files; identical files are a no-op. The `.json` spec and `.md` notes land under `state/sites/`. Keep that state private. Read the selected notes and operation description before calling it through the [pinned runner](api-anything.md). API Anything itself can have broader login, browser and write capabilities; the recipe installer does not constrain that runtime.

The directory's tested scope is narrow: bundled Amazon and Google Flights **search** operations have passed public reads, not purchase or booking. Frontier's learned **airports** operation passed; it does not cover reservations. United and Southwest remain browser references. DesignMD.app and shadcn/ui have their own listed tested read operations. A later status change requires fresh evidence, not a blanket inference from another operation.

Keep browsing history, captures, cookies, sessions, personal searches and any learned private recipes outside published packages. Do not turn a private operation into a public recipe or share a capture merely because a public directory mentions the site. The directory review checked identities, routes and selected operation behavior; it did not audit every site's security, terms, content or future availability.
