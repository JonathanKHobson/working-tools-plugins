(function () {
  "use strict";

  // Design Library's data adapter for the shared runtime/library-chooser UI.
  // Keep presentation generic while retaining the catalog's design-specific evidence.
  const node = document.getElementById("library-data") || document.getElementById("design-library-data");
  let data = {};
  try { data = JSON.parse(node ? node.textContent : "{}"); } catch (_) { data = {}; }
  const items = Array.isArray(data.items) ? data.items : [];
  const values = (item, key) => Array.isArray(item && item[key]) ? item[key] : [];
  const text = (item, key) => typeof (item && item[key]) === "string" ? item[key] : "";

  function searchText(item) {
    return [
      text(item, "id"), text(item, "name"), text(item, "summary"), text(item, "category"),
      ...values(item, "tags"), ...values(item, "bestFor"), ...values(item, "avoidWhen"),
      ...values(item, "interactions"), ...values(item, "limitations")
    ].join(" ");
  }

  function listText(valuesList) {
    return valuesList.length ? valuesList.map(value => "• " + value).join("\n") : "Not specified.";
  }

  window.LibraryAdapter = {
    title: "Design Templates",
    noun: "template",
    relatedLink: {
      label: "Video Library ↗",
      url: "https://library.jkylehobson.chatgpt.site/video-library/"
    },
    createLabel: "Create template",
    createTitle: "Create a design template",
    createDescription: "Describe the reusable design template you want to add to your library.",
    createPrompt: `Help me create a reusable Design Templates library entry, not just a one-off output. Preserve my brief and constraints; ask only for missing essentials such as purpose, audience, format, required interactions and visual references. Use the existing Design Templates authoring and review skills and the installed artifact-template package workflow, inspecting their current instructions rather than inventing an API.
Build a complete editable candidate with responsive source, realistic sample content, desktop/mobile previews, usage guidance and known limitations. For this Design Library, reusable Site packages use an artifact-template.json manifest with kind=site and reference=assets/source, plus catalog metadata: id, name, summary, category, tags, bestFor, avoidWhen, interactions, limitations, skillName and computed sourceHash. Inspect the existing schema and valid neighboring packages before registration; never invent a hash or overwrite an existing template.
Show the candidate for review, then add the reviewed template through the owning library workflow. If local authoring/registration tools are unavailable, provide a complete copyable/exportable candidate and exact remaining import steps, explaining what access is missing. Do not claim it is installed merely because this prompt was sent.
Success check: compare the rendered candidate with my references, exercise its key interaction and mobile layout, validate its package, and after registration verify its exact ID is discoverable in Design Templates and its preview and Use handoff work. Report prepared, saved, registered and verified states separately.`,
    items,
    detailType(item) {
      return text(item, "category");
    },
    filters: [
      {
        id: "category",
        label: "Type",
        type: "select",
        default: "all",
        options: [{ value: "all", label: "All types" }].concat(
          [...new Set(items.map(item => text(item, "category")).filter(Boolean))]
            .sort()
            .map(category => ({ value: category, label: category }))
        )
      },
      {
        id: "tag",
        label: "Need",
        type: "select",
        default: "all",
        options: [{ value: "all", label: "All needs" }].concat(
          [...new Set(items.flatMap(item => values(item, "tags")))].sort()
            .map(tag => ({ value: tag, label: tag }))
        )
      }
    ],
    searchText,
    matches(item, selected) {
      if (!selected) return true;
      if (selected.category && selected.category !== "all" && text(item, "category") !== selected.category) return false;
      return !selected.tag || selected.tag === "all" || values(item, "tags").includes(selected.tag);
    },
    preview(item) {
      return { image: text(item, "desktopPreview"), text: text(item, "summary") || text(item, "name") };
    },
    details(item) {
      const sections = [
        { label: "Summary", text: text(item, "summary") },
        { label: "Best for", text: listText(values(item, "bestFor")) },
        { label: "Think twice when", text: listText(values(item, "avoidWhen")) },
        { label: "Interactions", text: listText(values(item, "interactions")) },
        { label: "Known limits", text: listText(values(item, "limitations")) },
        { label: "Source", text: [text(item, "skillName"), text(item, "sourceHash")].filter(Boolean).join(" · ") }
      ];
      if (text(item, "desktopPreview")) sections.unshift({ label: "Desktop preview", image: text(item, "desktopPreview") });
      if (text(item, "mobilePreview")) sections.push({ label: "Mobile preview", image: text(item, "mobilePreview") });
      return sections;
    },
    localPrompt(item, brief) {
      return "Prepare a verified Design Library handoff for " + text(item, "name") + " (ID: " + text(item, "id") + ").\n" +
        "Brief: " + (brief || "(none supplied)") + "\n" +
        "Call prepare_design_handoff with template_id=\"" + text(item, "id") + "\" and this brief. Verify the current installed source and source hash before adapting a new copy through Sites. Source validation was unavailable in this chooser.";
    },
    handoff: {
      tool: "prepare_design_handoff",
      args(item, brief) {
        return { template_id: text(item, "id"), brief: brief || "" };
      },
      text(payload, item) {
        if (!payload || payload.templateId !== item.id || payload.sourceHash !== item.sourceHash || payload.mode !== "complete-template" || typeof payload.handoffText !== "string" || !payload.handoffText.trim()) {
          throw new Error("The host returned an incomplete or mismatched design handoff.");
        }
        return payload.handoffText;
      }
    }
  };
})();
