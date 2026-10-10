(function () {
  "use strict";

  const data = JSON.parse(document.getElementById("library-data").textContent);
  const briefs = Array.isArray(data.briefs) ? data.briefs : [];
  const typeNames = {
    legacy_profile: "Existing profile",
    voice_candidate: "Voice candidate",
    module: "Module",
    alias: "Alias",
    merge: "Merge"
  };

  function route(item) {
    const selected = item.route || {};
    const modules = Array.isArray(selected.module_ids) ? selected.module_ids : [];
    return String(selected.base_profile_id || item.id) + (modules.length ? " + " + modules.join(" + ") : "");
  }

  function example(item, values) {
    const samples = item.examples || [];
    if (values && values.brief) return samples.find(sample => sample.brief_id === values.brief);
    return samples[0];
  }

  function cleanProse(text) {
    return text.replace(/^#{1,6}\s+/gm, "").replace(/\*\*([^*]+)\*\*/g, "$1").replace(/(?<!\*)\*([^*\n]+)\*(?!\*)/g, "$1");
  }

  window.LibraryAdapter = {
    title: "Writing Templates",
    noun: "template",
    createLabel: "Create template",
    createTitle: "Create a writing template",
    items: data.items,
    detailType(item) {
      return typeNames[item.resource_type] || item.resource_type;
    },
    filters: [
      {
        id: "type",
        label: "Type",
        type: "select",
        default: "all",
        options: [
          { value: "all", label: "All resources" },
          { value: "legacy_profile", label: "Existing profiles" },
          { value: "voice_candidate", label: "Voice candidates" },
          { value: "module", label: "Modules" },
          { value: "alias", label: "Aliases" },
          { value: "merge", label: "Merges" }
        ]
      },
      {
        id: "brief",
        label: "Preview example",
        type: "select",
        default: "",
        previewOnly: true,
        options: [{ value: "", label: "Template example" }, ...briefs.map(brief => ({ value: brief.id, label: brief.name }))]
      }
    ],
    searchText(item) {
      return [item.id, item.name, item.description, item.mechanism, item.primary_layer, ...(item.tags || [])].join(" ");
    },
    matches(item, values) {
      return !values || !values.type || values.type === "all" || item.resource_type === values.type;
    },
    preview(item, values) {
      const selected = example(item, values);
      return { image: item.coverImage, imageFit: "contain", text: selected ? cleanProse(selected.text) : "Verified example unavailable." };
    },
    details(item, values) {
      const selected = example(item, values);
      const sections = [
        { label: "Resource", text: (typeNames[item.resource_type] || item.resource_type) + " · " + item.id + " · v" + item.version },
        { label: "Description", text: item.description },
        { label: "Example", text: selected ? selected.text : "Verified example unavailable." },
        { label: "Actual route", text: route(item) },
        { label: "Movement", text: item.mechanism }
      ];
      if (item.rhythm) sections.push({ label: "Rhythm", text: item.rhythm });
      if (item.neighbor_difference) sections.push({ label: "Difference from neighbors", text: item.neighbor_difference });
      if (item.evidence_status) sections.push({ label: "Evidence status", text: item.evidence_status.replaceAll("_", " ") });
      if (item.truth_boundary) sections.push({ label: "Truth boundary", text: item.truth_boundary });
      if (item.research) {
        if (item.research.authoring_implication) sections.push({ label: "Research context", text: item.research.authoring_implication });
        if (item.research.limits) sections.push({ label: "Research limits", text: item.research.limits });
      }
      if (data.briefsText) sections.push({ label: "Shared brief and protected facts", text: data.briefsText });
      if (item.sourceUri) sections.push({ label: "Public source", href: item.sourceUri });
      return sections;
    },
    localPrompt(item, brief) {
      return "Prepare a verified Writing Voice Library handoff for " + item.id + " (v" + item.version + "), actual route " + route(item) + ".\nPublic source: " + item.sourceUri + "\nBrief: " + (brief || "(none supplied)") + "\nCall prepare_writing_voice_handoff with profile_id " + item.id + " and this brief. Verify current catalog, guide and sample hashes before drafting. Source validation was unavailable in this chooser.";
    },
    handoff: {
      tool: "prepare_writing_voice_handoff",
      args(item, brief) {
        return { profile_id: item.id, brief: brief || "", modifier_ids: [] };
      },
      text(payload, item) {
        if (!payload || payload.profileId !== item.id || payload.version !== item.version || payload.state !== "prepared" || typeof payload.handoffText !== "string" || !payload.handoffText.trim()) {
          throw new Error("The host returned an incomplete or mismatched writing handoff.");
        }
        return payload.handoffText;
      }
    },
    createPrompt: "Help me create a reusable writing template for my Writing Templates library using the existing create-writing-voice skill and current catalog workflow. Preserve my instructions; ask only for missing essentials such as purpose, audience, tone, format and an example or reference. Inspect the current schema and nearby entries before authoring.\nDevelop a complete candidate with a name, intended uses, limits, actionable voice guidance and original sample prose. Reuse a suitable existing base or module when appropriate; keep source provenance and distinguish tested behavior from proposed guidance. Show me the candidate for review before registering it. If authoring or catalog tools are unavailable, provide the complete copyable candidate and exact remaining import steps.\nSuccess check: test the candidate on a representative brief, check that its guidance and sample agree, validate required catalog fields and, after approved registration, verify its exact ID appears in Writing Templates and that View and Use work. Report candidate, saved, registered and verified states separately; sending this prompt is not registration.",
  };
})();
