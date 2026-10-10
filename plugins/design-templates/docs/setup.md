# Setup with your own source collection

Create a Python 3.10+ environment and install requirements.txt. Set DESIGN_LIBRARY_PYTHON to its executable, or use the existing external interpreter binding described by the launcher. The stock Python bootstrap is stdlib-only and executes the selected environment before the server imports MCP.

Supply DESIGN_LIBRARY_CATALOG as the absolute path to a compatible Site catalog.json and DESIGN_TEMPLATES_DATA_ROOT as a source root containing templates/<skillName>/assets/source, each artifact-template.json, DESIGN.md, WORKFLOW.md and provenance/template-assets.json. The catalog's directory supplies assets/<id>-desktop.png and assets/<id>-mobile.png. Exact source and guidance hashes are verified before a handoff. Symlinks, changed sources and unanchored guidance remain rejected.

To inspect an authored fixture, run the selected Python with scripts/create_sample_collection.py --output <empty-external-folder>, then set the two emitted environment values before enabling the plugin. No private template is used. The default empty catalog can start but cannot claim a useful source selection until data is bound.

The full-format inventory and recipe CLI reads templates/catalog.json and templates/adaptation-recipes.json beneath DESIGN_TEMPLATES_DATA_ROOT. Token checks accept your explicit source paths. Existing Documents, Presentations, Spreadsheets and Sites providers retain adaptation/export ownership; this plugin supplies neither provider code nor the original private references.

Optional private search feedback can use DESIGN_LIBRARY_FEEDBACK_DB outside this package or an existing external Atlas binding. Without either binding, the three Design Library tools remain usable and no feedback persistence is claimed. The bundled helper supplies the complete two feedback tools when explicitly configured. No external Python module is loaded from a host binding.

Portable mcp.json uses PLUGIN_ROOT; compatibility .mcp.json uses CLAUDE_PLUGIN_ROOT. Both launch the same complete local stdio server. MCP App support is separate from text-tool access; standalone HTML export does not prove live host interaction.
