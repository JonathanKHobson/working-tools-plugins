import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const catalog = JSON.parse(await readFile(path.join(here, "data/catalog.json"), "utf8"));
const assemblyCode = await readFile(path.join(here, "data/assembly.js"), "utf8");
const sourcePath = process.env.PROMPT_FRAMEWORK_SOURCE;
if (!sourcePath) throw new Error("Set PROMPT_FRAMEWORK_SOURCE to the matching authorized framework source before this lineage check.");
const source = await readFile(sourcePath, "utf8");
const sourceHash = createHash("sha256").update(source).digest("hex");
assert.equal(catalog.sourceCoverage.sourceSha256, sourceHash, "Generated catalog source hash drifted");
assert.equal(catalog.items.length, catalog.sourceCoverage.catalogItems);
assert.equal(new Set(catalog.items.map((item) => item.id)).size, catalog.items.length);
assert.equal(catalog.items.filter((item) => item.notice).length, 34, "Source notices were lost");
assert.equal(catalog.items.filter((item) => item.related.length).length, 9, "Source related links were lost");
const allFields = catalog.items.flatMap((item) => item.fields);
assert.equal(allFields.filter((field) => field.dataset).length, 10, "Field dataset metadata was lost");
assert.equal(allFields.filter((field) => field.unit).length, 10, "Field unit metadata was lost");
assert.equal(allFields.filter((field) => field.autofill).length, 169, "Field autofill metadata was lost");
const okrGroup = catalog.items.find((item) => item.id === "okr-goal-setting").fields.find((field) => field.key === "key_results");
assert.equal(okrGroup.itemType, "group");
assert.equal(okrGroup.fields.length, 10);

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(assemblyCode, sandbox, { timeout: 10_000, filename: "assembly.js" });
assert.equal(sandbox.window.PromptAssembly.ids.length, catalog.items.length);

const emptyErrors = [];
const populatedErrors = [];
const missingSentinels = [];
const notStrings = [];

for (const item of catalog.items) {
  const id = item.id;
  sandbox.testId = id;
  sandbox.testValues = {};
  try {
    const result = vm.runInContext("window.PromptAssembly.assemble(testId, testValues)", sandbox, { timeout: 300 });
    if (typeof result !== "string") notStrings.push(id);
  } catch (error) { emptyErrors.push({ id, error: String(error.message) }); }

  const input = {};
  for (const field of item.fields) {
    if (!field.key) continue;
    input[field.key] = field.type === "repeater" && field.itemType === "group"
      ? [Object.fromEntries(field.fields.map((child) => [child.key, `ZZ_${child.key.replace(/[^A-Za-z0-9]/g, "_")}_END`]))]
      : `ZZ_${field.key.replace(/[^A-Za-z0-9]/g, "_")}_END`;
  }
  input.ctx = "ZZ_COMMON_CONTEXT_END";
  sandbox.testValues = input;
  try {
    const result = vm.runInContext("window.PromptAssembly.assemble(testId, testValues)", sandbox, { timeout: 300 });
    if (typeof result !== "string") { notStrings.push(id); continue; }
    const absent = Object.entries(input).filter(([key, token]) => key !== "ctx" && !Array.isArray(token) &&
      !result.includes(token)).map(([key]) => key);
    if (absent.length) missingSentinels.push({ id, fields: absent });
  } catch (error) { populatedErrors.push({ id, error: String(error.message) }); }
}

function assemble(id, values) {
  sandbox.testId = id;
  sandbox.testValues = values;
  return vm.runInContext("window.PromptAssembly.assemble(testId, testValues)", sandbox, { timeout: 300 });
}
const clear = assemble("clear-path-forward-framework", {
  concise: "Summarize the report", logical: "Read findings before recommendations",
  explicit: "Three bullets", adaptive: "For a busy director", reflective: "Flag uncertainty",
});
assert.match(clear, /Summarize the report/);
assert.match(clear, /Three bullets/);
const repaired = assemble("small-artifact-advantage", {
  claim: "I can teach AI literacy", audience: "Hiring committee",
  artifact_type: "one-page memo", evidence: "Sample lesson", caveat: "Personal sample", route: "Portfolio",
});
for (const value of ["I can teach AI literacy", "Hiring committee", "one-page memo", "Sample lesson", "Personal sample", "Portfolio"]) {
  assert.ok(repaired.includes(value), `Small Artifact adaptation omitted ${value}`);
}
assert.ok(!repaired.includes("Claim to prove: claim"), "Source literal-value defect leaked into the adaptation");
const hypnagogic = assemble("hypnagogic-spark-creativity", { problem: "Find a new workshop hook", success_metric: "Three viable ideas" });
assert.match(hypnagogic, /Success metric: Three viable ideas/);
const okr = assemble("okr-goal-setting", {
  objective: "Help new members reach their first success",
  key_results: [{ metric: "Time to first success", baseline: "14 days", target: "4 days", type: "lagging", timeframe: "Q4", owner: "Onboarding PM", instrument: "Analytics event", guardrail: "CSAT at least 4.5", risks: "Seasonality", initiatives: "Guided setup" }],
});
for (const value of ["Time to first success", "14 days", "4 days", "Analytics event", "CSAT at least 4.5", "Guided setup"]) {
  assert.ok(okr.includes(value), `OKR group omitted ${value}`);
}
assert.throws(() => assemble("okr-goal-setting", { key_results: "Metric: Time to first success" }), /Structured group items required/);
const tarot = assemble("tarot-spread-reflection", { reversals: false, action_bias: true, confidence_block: true });
assert.equal(typeof tarot, "string");

console.log(JSON.stringify({
  sourceRecords: catalog.sourceCoverage.sourceRecords,
  catalogItems: catalog.items.length,
  emptyErrorCount: emptyErrors.length,
  emptyErrors: emptyErrors.slice(0, 15),
  populatedErrorCount: populatedErrors.length,
  populatedErrors: populatedErrors.slice(0, 15),
  notStrings,
  missingSentinels: missingSentinels.slice(0, 5),
  missingSentinelItems: missingSentinels.length,
}, null, 2));

assert.equal(emptyErrors.length, 0, "Some source functions failed with empty values");
assert.equal(populatedErrors.length, 0, "Some source functions failed with populated values");
assert.equal(notStrings.length, 0, "Some source functions returned non-text");
