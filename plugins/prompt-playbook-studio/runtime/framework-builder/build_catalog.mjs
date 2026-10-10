// Static projection of the reviewed local AI Glossary framework array. The
// source wrapper and its eval-based hydration are deliberately never run.
import { createHash } from "node:crypto";
import { readFile, mkdir, writeFile, readdir } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const sourcePath = process.env.PROMPT_FRAMEWORK_SOURCE;
if (!sourcePath) throw new Error("Set PROMPT_FRAMEWORK_SOURCE to a recipient-owned framework source file before rebuilding.");
const parserRoot = process.env.PROMPT_PARSER_ROOT;
if (!parserRoot) throw new Error("Set PROMPT_PARSER_ROOT to a Node modules directory with @babel/parser, @babel/traverse and js-yaml.");
const parser = require(path.join(parserRoot, "@babel/parser"));
const traverse = require(path.join(parserRoot, "@babel/traverse")).default;

const sourceRel = "glossary/js/templates.data.js";
const approvedSourceSha256 = "2c1b4f82f9aed48d8fe9c586653e5192ed0c7348b4603528a558a96030264d51";
const atlasRoot = process.env.PROMPT_ATLAS_ROOT;
if (!atlasRoot) throw new Error("Set PROMPT_ATLAS_ROOT to a recipient-owned Atlas pattern directory.");
const yaml = require(path.join(parserRoot, "js-yaml"));
const allowedGlobals = new Set([
  "Boolean", "String", "Array", "Math", "Number", "Object", "isNaN",
  "parseFloat", "isFinite", "Set", "Infinity", "RegExp", "parseInt", "NaN", "Map",
]);
const forbiddenProperty = new Set(["constructor", "prototype", "__proto__"]);
const forbiddenCall = new Set(["eval", "Function", "fetch", "require", "importScripts"]);
const maxInputLength = 12_000;
const maxOutputLength = 250_000;
const arrayPrimaryIds = [
  "empty-chair-technique", "par-problem-action-result", "parts-work-dialogue",
  "rasa-dhvani-planner", "confucian-deliberation-harmony-face-ritual",
  "two-eyed-seeing", "indigenous-storywork-coast-salish-stolo",
];
const arrayFieldOverrides = { "parts-work-dialogue": ["grounding_presets"] };
const pickerAdaptation = `({goal,stage,deliverable,constraints,include,exclude,ctx}) => {
  const words = String([goal,deliverable,constraints].filter(Boolean).join(' ')).toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
  const included = String(include || '').toLowerCase().split(/[,\\s]+/).filter(Boolean);
  const excluded = String(exclude || '').toLowerCase().split(/[,\\s]+/).filter(Boolean);
  const candidates = pickerIndex.filter(item => !excluded.some(tag => item.tags.some(t => t.toLowerCase().includes(tag))));
  const ranked = candidates.map(item => {
    const uses = item.use_cases.join(' ').toLowerCase();
    const tags = item.tags.join(' ').toLowerCase();
    const text = [item.label,item.definition,item.help,item.categories.join(' ')].join(' ').toLowerCase();
    const score = words.reduce((total,word) => total + (uses.includes(word) ? 5 : 0) + (tags.includes(word) ? 2 : 0) + (text.includes(word) ? 1 : 0),0)
      + included.reduce((total,tag) => total + (tags.includes(tag) ? 3 : 0),0);
    return { item, score };
  }).sort((a,b) => b.score - a.score || a.item.label.localeCompare(b.item.label)).slice(0,7);
  return [
    'Pattern Picker — choose a source framework or pattern.',
    ctx && 'Context: ' + ctx,
    goal && 'Goal: ' + goal,
    stage && 'Stage: ' + stage,
    deliverable && 'Desired deliverable: ' + deliverable,
    constraints && 'Constraints: ' + constraints,
    included.length && 'Prefer tags: ' + included.join(', '),
    excluded.length && 'Exclude tags: ' + excluded.join(', '),
    'Candidate source frameworks:',
    ...ranked.map(row => '- ' + row.item.label + ' (' + row.item.slug + ')'),
    'Recommend one best fit with a short rationale, name two alternates, then draft a ready-to-copy prompt using the chosen framework. Ask up to three clarifying questions only if essential.'
  ].filter(Boolean).join('\\n');
}`;
const smallArtifactAdaptation = `({claim,audience,artifact_type,evidence,caveat,route}) => [
  'Use Small Artifact Advantage to produce a practical communication scaffold.',
  claim && 'Claim to prove: ' + claim,
  audience && 'Audience: ' + audience,
  artifact_type && 'Artifact type: ' + artifact_type,
  evidence && 'Evidence available: ' + evidence,
  caveat && 'Scope caveat: ' + caveat,
  route && 'Distribution route: ' + route,
  'Return:',
  'A filled scaffold with gaps marked [MISSING].',
  'A recommended next communication action.',
  'Risks, caveats, or ethical guardrails to keep visible.'
].filter(Boolean).join('\\n')`;

function sha(value) {
  return createHash("sha256").update(value).digest("hex");
}

function extractArray(source) {
  const marker = "const arr = ";
  const offset = source.indexOf(marker);
  if (offset < 0) throw new Error("Expected framework array marker is absent");
  const start = source.indexOf("[", offset + marker.length);
  if (start < 0) throw new Error("Expected framework array is absent");
  let depth = 0, quoted = false, escaped = false;
  for (let i = start; i < source.length; i++) {
    const ch = source[i];
    if (quoted) {
      if (escaped) escaped = false;
      else if (ch === "\\") escaped = true;
      else if (ch === '"') quoted = false;
      continue;
    }
    if (ch === '"') { quoted = true; continue; }
    if (ch === "[") depth++;
    if (ch === "]" && --depth === 0) {
      const tail = source.slice(i + 1);
      if (!/^\s*\.map\(t\s*=>\s*\(\{\.\.\.t,\s*template:\s*t\.template\s*\?\s*\(0, eval\)/.test(tail)) {
        throw new Error("Source wrapper changed; inspect before rebuilding");
      }
      return JSON.parse(source.slice(start, i + 1));
    }
  }
  throw new Error("Unclosed framework array");
}

function stringArray(values) {
  return Array.isArray(values) ? values.filter((v) => typeof v === "string") : [];
}

function normalizeField(field) {
  const options = Array.isArray(field.options) ? field.options.map((option) =>
    option && typeof option === "object"
      ? { label: String(option.label ?? option.value ?? ""), value: String(option.value ?? option.label ?? "") }
      : { label: String(option), value: String(option) }) : [];
  const result = {
    key: String(field.key || ""),
    label: String(field.label || field.key || "Input"),
    type: String(field.type || "text"),
    placeholder: String(field.ph || field.placeholder || ""),
    description: String(field.desc || ""),
    options,
    required: field.required === true,
  };
  for (const key of ["def", "min", "max", "itemLabel", "itemType", "blockJoin", "dataset", "unit", "autofill"]) {
    if (Object.hasOwn(field, key)) result[key === "def" ? "default" : key] = field[key];
  }
  if (Array.isArray(field.fields)) result.fields = field.fields.map(normalizeField);
  return result;
}

function inspectTemplate(source, slug) {
  const expression = slug === "pattern-picker" ? pickerAdaptation :
    slug === "small-artifact-advantage" ? smallArtifactAdaptation :
    slug === "hypnagogic-spark-creativity"
      ? `(f) => { const result = (${source})(f); return f.success_metric ? result + '\\nSuccess metric: ' + f.success_metric : result; }`
      : source;
  const ast = parser.parse(`const __template = (${expression});`, { sourceType: "script" });
  const fn = ast.program.body[0].declarations[0].init;
  if (fn.type !== "ArrowFunctionExpression" && fn.type !== "FunctionExpression") {
    throw new Error(`${slug}: template is not a function expression`);
  }
  const violations = [];
  const reject = (why) => { if (violations.length < 8) violations.push(why); };
  traverse(ast, {
    ReferencedIdentifier(p) {
      const name = p.node.name;
      if (!p.scope.hasBinding(name, true) && !allowedGlobals.has(name) &&
          !(slug === "pattern-picker" && name === "pickerIndex")) {
        reject(`unbound identifier ${name}`);
      }
    },
    MemberExpression(p) {
      const prop = p.node.property;
      if (!p.node.computed && forbiddenProperty.has(prop.name)) reject(`forbidden member ${prop.name}`);
      if (p.node.computed && (prop.type === "StringLiteral" || prop.type === "Literal") &&
          forbiddenProperty.has(String(prop.value))) reject(`forbidden computed member ${prop.value}`);
    },
    OptionalMemberExpression(p) {
      const prop = p.node.property;
      if (!p.node.computed && forbiddenProperty.has(prop.name)) reject(`forbidden optional member ${prop.name}`);
      if (p.node.computed && prop.type === "StringLiteral" && forbiddenProperty.has(prop.value)) {
        reject(`forbidden computed optional member ${prop.value}`);
      }
    },
    CallExpression(p) {
      const callee = p.node.callee;
      if (callee.type === "Identifier" && forbiddenCall.has(callee.name)) reject(`forbidden call ${callee.name}`);
      if ((callee.type === "MemberExpression" || callee.type === "OptionalMemberExpression") &&
          !callee.computed && forbiddenCall.has(callee.property.name)) reject(`forbidden method ${callee.property.name}`);
    },
    NewExpression(p) {
      if (p.node.callee.type !== "Identifier" || !["Set", "Map", "RegExp"].includes(p.node.callee.name)) {
        reject("unreviewed constructor");
      }
    },
    ThisExpression() { reject("this expression"); },
    Super() { reject("super expression"); },
    Import() { reject("dynamic import"); },
    WithStatement() { reject("with statement"); },
  });
  if (violations.length) throw new Error(`${slug}: ${violations.join(", ")}`);
  return expression;
}

const source = await readFile(sourcePath, "utf8");
if (sha(source) !== approvedSourceSha256) {
  throw new Error("Framework source hash changed; repeat security review before rebuilding");
}
const rawItems = extractArray(source);
async function readAtlasEntries(dir) {
  const output = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) output.push(...await readAtlasEntries(full));
    else if (entry.isFile() && /^pattern--.*\.md$/.test(entry.name)) {
      const body = await readFile(full, "utf8");
      if (!body.startsWith("---\n")) continue;
      const close = body.indexOf("\n---\n", 4);
      if (close < 0) continue;
      const frontmatter = yaml.load(body.slice(4, close));
      if (frontmatter && typeof frontmatter === "object") output.push({ path: full, body, frontmatter });
    }
  }
  return output;
}
const atlasEntries = await readAtlasEntries(atlasRoot);
const atlasBySlug = new Map();
for (const entry of atlasEntries) {
  const slug = entry.frontmatter.source_slug;
  if (!slug) continue;
  if (atlasBySlug.has(slug)) throw new Error(`Duplicate Atlas source_slug: ${slug}`);
  atlasBySlug.set(slug, entry);
}
const seenSlugs = new Map();
const seenIds = new Set();
const duplicateSlugs = [];
const items = [];
const assemblyEntries = [];
const pickerIndex = [];

for (const raw of rawItems) {
  if (!raw || typeof raw !== "object" || !raw.slug || !raw.id || !raw.label || typeof raw.template !== "string") {
    throw new Error("Malformed framework record");
  }
  const baseSlug = String(raw.slug);
  const ordinal = (seenSlugs.get(baseSlug) || 0) + 1;
  seenSlugs.set(baseSlug, ordinal);
  const id = ordinal === 1 ? baseSlug : `${baseSlug}~${ordinal}`;
  if (ordinal > 1) duplicateSlugs.push({ slug: baseSlug, assignedId: id, sourceId: raw.id });
  if (seenIds.has(id)) throw new Error(`Duplicate generated ID: ${id}`);
  seenIds.add(id);
  const expression = inspectTemplate(raw.template, baseSlug);
  const atlas = atlasBySlug.get(baseSlug);
  if (!atlas) throw new Error(`No active Atlas pattern for ${baseSlug}`);
  const atlasMeta = atlas.frontmatter;
  const fields = Array.isArray(raw.fields) ? raw.fields.map(normalizeField) : [];
  const item = {
    id,
    name: String(raw.label),
    slug: baseSlug,
    kind: String(raw.kind || "framework"),
    definition: String(raw.definition || ""),
    help: String(raw.help || ""),
    categories: stringArray(raw.categories),
    tags: stringArray(raw.tags),
    useCases: stringArray(raw.use_cases),
    boosters: stringArray(raw.boosters),
    notice: String(raw.notice || ""),
    related: stringArray(raw.related),
    fields,
    facets: raw.facets && typeof raw.facets === "object" ? raw.facets : {},
    assemblyStatus: baseSlug === "pattern-picker" ? "adapted-static-index" :
      ["small-artifact-advantage", "hypnagogic-spark-creativity"].includes(baseSlug) ? "adapted-source-defect" :
      arrayPrimaryIds.includes(baseSlug) ? "authored-function-repeater-adaptation" : "authored-function",
    assemblyNote: baseSlug === "small-artifact-advantage"
      ? "The inherited template passes field names as literal values for six inputs. This reviewed adaptation inserts each actual field value while preserving the source return instructions."
      : baseSlug === "hypnagogic-spark-creativity"
      ? "The inherited template omits its success_metric field. This reviewed adaptation appends the supplied metric."
      : baseSlug === "pattern-picker"
      ? "Reviewed local static index replaces source code that reads window.FRAMEWORKS."
      : "",
    atlas: {
      path: String(atlasMeta.canonical_path || path.relative(path.dirname(atlasRoot), atlas.path)),
      sha256: sha(atlas.body),
      status: String(atlasMeta.status || "unknown"),
      browseGroup: String(atlasMeta.browse_group || ""),
      domains: stringArray(atlasMeta.personal_domains),
      workflowRoles: stringArray(atlasMeta.workflow_roles),
      searchBoostTerms: stringArray(atlasMeta.search_boost_terms),
      personalSurface: atlasMeta.personal_surface === true,
      practicalPriority: String(atlasMeta.practical_priority || ""),
    },
    source: {
      path: sourceRel,
      sha256: sha(source),
      recordSha256: sha(JSON.stringify(raw)),
      templateSha256: sha(raw.template),
      emittedTemplateSha256: sha(expression),
      status: "inherited-unreviewed",
      sourceId: String(raw.id),
      sourceSlug: baseSlug,
      ordinal,
    },
  };
  items.push(item);
  assemblyEntries.push(`${JSON.stringify(id)}: (${expression})`);
  pickerIndex.push({ id: raw.id, slug: raw.slug, label: raw.label,
    definition: raw.definition || "", help: raw.help || "", tags: raw.tags || [],
    categories: raw.categories || [], use_cases: raw.use_cases || [] });
}

const catalog = {
  schemaVersion: 1,
  sourceCoverage: {
    source: sourceRel,
    sourceSha256: sha(source),
    sourceRecords: rawItems.length,
    catalogItems: items.length,
    assemblyFunctions: assemblyEntries.length,
    duplicateSlugs,
    atlasEntries: atlasEntries.length,
    atlasMatchedSlugs: seenSlugs.size,
    atlasOnlySlugs: atlasEntries.map((entry) => entry.frontmatter.source_slug).filter((slug) => slug && !seenSlugs.has(slug)).sort(),
    arrayPrimaryAdaptations: arrayPrimaryIds,
    arrayFieldOverrides,
    excludedTaskSource: "glossary/js/templates.tasks.data.js",
    note: "Framework, pattern, strategy, heuristic, technique, tool, facilitation, and helper records only. Task templates are a separate source lane.",
  },
  items,
};

const assembly = `// Generated by runtime/framework-builder/build_catalog.mjs from a reviewed local source.\n` +
`// The source wrapper and its eval call are excluded. Do not edit this file by hand.\n` +
`(function (host) {\n` +
`  "use strict";\n` +
`  const pickerIndex = ${JSON.stringify(pickerIndex)};\n` +
`  const templates = {\n    ${assemblyEntries.join(",\n    ")}\n  };\n` +
`  const arrayPrimaryIds = new Set(${JSON.stringify(arrayPrimaryIds)});\n` +
`  const arrayFieldOverrides = ${JSON.stringify(arrayFieldOverrides)};\n` +
`  const fieldKinds = ${JSON.stringify(Object.fromEntries(items.map((item) => [item.id, item.fields.map((field) => ({ key: field.key, type: field.type, itemType: field.itemType || "", blockJoin: field.blockJoin || "", fields: field.fields?.map((child) => ({ key: child.key, type: child.type })) || [] }))])))};\n` +
`  function assemble(id, values = {}) {\n` +
`    if (!Object.hasOwn(templates, id)) throw new Error("Unknown framework: " + String(id));\n` +
`    if (!values || typeof values !== "object" || Array.isArray(values)) throw new TypeError("Framework values must be an object");\n` +
`    const merged = Object.create(null);\n` +
`    let totalInputLength = 0;\n` +
`    for (const field of fieldKinds[id]) {\n` +
`      if (!Object.hasOwn(values, field.key)) continue;\n` +
`      const raw = values[field.key];\n` +
`      if (field.type === "repeater" && field.itemType === "group") {\n` +
`        if (!Array.isArray(raw)) throw new TypeError("Structured group items required: " + field.key);\n` +
`        if (raw.length > 20) throw new RangeError("Too many group items: " + field.key);\n` +
`        const groups = raw.map((entry) => {\n` +
`          if (!entry || typeof entry !== "object" || Array.isArray(entry)) throw new TypeError("Group item must be an object: " + field.key);\n` +
`          const projected = Object.create(null);\n` +
`          for (const child of field.fields) {\n` +
`            if (!Object.hasOwn(entry, child.key)) continue;\n` +
`            const value = String(entry[child.key] ?? "");\n` +
`            if (value.length > ${maxInputLength}) throw new RangeError("Group input is too long: " + child.key);\n` +
`            totalInputLength += value.length;\n` +
`            if (totalInputLength > 100000) throw new RangeError("Framework inputs are too long");\n` +
`            projected[child.key] = value;\n` +
`          }\n` +
`          return projected;\n` +
`        });\n` +
`        merged[field.key] = groups;\n` +
`        merged[field.key + "_list"] = groups;\n` +
`        merged[field.key + "_items"] = groups;\n` +
`        merged[field.key + "_arr"] = groups;\n` +
`        continue;\n` +
`      }\n` +
`      const text = Array.isArray(raw) ? raw.map(String).join("\\n") : String(raw ?? "");\n` +
`      if (text.length > ${maxInputLength}) throw new RangeError("Framework input is too long: " + field.key);\n` +
`      totalInputLength += text.length;\n` +
`      if (totalInputLength > 100000) throw new RangeError("Framework inputs are too long");\n` +
`      if (Array.isArray(raw) && raw.length > 100) throw new RangeError("Framework list is too long: " + field.key);\n` +
`      merged[field.key] = field.type === "checkbox" ? raw === true || raw === "true" : text;\n` +
`      if (arrayFieldOverrides[id]?.includes(field.key)) merged[field.key] = Array.isArray(raw) ? raw.map(String) : text.split(/\\n+/).filter(Boolean);\n` +
`      if (field.type === "repeater" || field.type === "dynamic_tasks") {\n` +
`        const blocky = field.itemType === "typeahead_textarea" || field.itemType === "textarea" || field.blockJoin === "---";\n` +
`        const list = (Array.isArray(raw) ? raw.map(String) : text.split(blocky ? /\\n\\s*---\\s*\\n/ : /\\n+/)).map((s) => s.trim()).filter(Boolean);\n` +
`        if (list.length > 100) throw new RangeError("Framework list is too long: " + field.key);\n` +
`        if (arrayPrimaryIds.has(id)) merged[field.key] = list;\n` +
`        merged[field.key + "_list"] = list;\n` +
`        merged[field.key + "_items"] = list;\n` +
`        merged[field.key + "_arr"] = list;\n` +
`        if (/s$/.test(field.key) && list.length === 1 && !Object.hasOwn(merged, field.key.slice(0, -1))) merged[field.key.slice(0, -1)] = list[0];\n` +
`      }\n` +
`    }\n` +
`    for (const key of ["ctx", "audience", "style", "tone", "bias_awareness_block", "bias_mitigations_block", "ethics_block", "bias_directives"]) {\n` +
`      if (!Object.hasOwn(values, key)) continue;\n` +
`      if (Object.hasOwn(merged, key)) continue;\n` +
`      const text = String(values[key] ?? "");\n` +
`      if (text.length > ${maxInputLength}) throw new RangeError("Framework input is too long: " + key);\n` +
`      totalInputLength += text.length;\n` +
`      if (totalInputLength > 100000) throw new RangeError("Framework inputs are too long");\n` +
`      merged[key] = text;\n` +
`    }\n` +
`    const result = templates[id](merged);\n` +
`    if (typeof result !== "string") throw new TypeError("Framework did not return text: " + id);\n` +
`    if (result.length > ${maxOutputLength}) throw new RangeError("Framework output is too long: " + id);\n` +
`    return result;\n` +
`  }\n` +
`  host.PromptAssembly = Object.freeze({ assemble, ids: Object.freeze(Object.keys(templates)) });\n` +
`})(window);\n`;

catalog.sourceCoverage.assemblySha256 = sha(assembly);

await mkdir(path.join(here, "data"), { recursive: true });
await writeFile(path.join(here, "data/catalog.json"), JSON.stringify(catalog) + "\n");
await writeFile(path.join(here, "data/assembly.js"), assembly);
console.log(`Projected ${items.length} framework records with ${assemblyEntries.length} static functions; ${duplicateSlugs.length} duplicate slug(s).`);
