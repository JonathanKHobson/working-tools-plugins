/*
 * Shared benchmark dataset — SYNTHETIC. All figures are fictional demonstration
 * data, not Kyle's results and not any real program's results.
 *
 * Used unchanged by examples/baseline, examples/workbench and examples/editorial.
 * Plain classic script (no modules) so every example opens from file:// with a
 * relative <script src>. Consumers must not mutate these records; scenarios are
 * held as separate overlays.
 *
 * Fields (per shared/benchmark-brief.md):
 *   id, title, week (1..8), enrollment, capacity, rating (1..5), response_count, cost_usd
 * Missing-data convention: S12's feedback survey has not closed, so
 *   response_count = 0 and rating = null ("no ratings yet"), never 0.
 *
 * Reference answers (hand-computed, for checks — see evaluation.md):
 *   total enrollment 217, total capacity 316, pooled occupancy 68.7%
 *   below 60% occupancy: S04 45.8%, S06 50.0%, S09 45.0%, S11 59.1%, S12 50.0%
 *   boundary: S08 is exactly 60.0% and is NOT below 60%
 */
window.SESSION_DATA = Object.freeze([
  { id: "S01", title: "Orientation to Inclusive Research", week: 1, enrollment: 28, capacity: 30, rating: 4.4, response_count: 22, cost_usd: 1200 },
  { id: "S02", title: "Survey Question Design",            week: 1, enrollment: 19, capacity: 30, rating: 4.1, response_count: 9,  cost_usd: 900 },
  { id: "S03", title: "Heuristic Evaluation Lab",          week: 2, enrollment: 22, capacity: 25, rating: 4.6, response_count: 18, cost_usd: 1100 },
  { id: "S04", title: "Task Analysis Studio",              week: 3, enrollment: 11, capacity: 24, rating: 3.2, response_count: 5,  cost_usd: 1000 },
  { id: "S05", title: "Prototyping Fidelity Clinic",       week: 3, enrollment: 19, capacity: 20, rating: 4.8, response_count: 16, cost_usd: 850 },
  { id: "S06", title: "Accessible Data Displays",          week: 4, enrollment: 16, capacity: 32, rating: 4.5, response_count: 4,  cost_usd: 1300 },
  { id: "S07", title: "Displays and Controls",             week: 4, enrollment: 24, capacity: 30, rating: 3.9, response_count: 20, cost_usd: 950 },
  { id: "S08", title: "Writing for Interfaces",            week: 5, enrollment: 15, capacity: 25, rating: 4.0, response_count: 12, cost_usd: 700 },
  { id: "S09", title: "Usability Testing Practicum",       week: 6, enrollment: 9,  capacity: 20, rating: 4.2, response_count: 6,  cost_usd: 1400 },
  { id: "S10", title: "Emotion in Task Analysis",          week: 6, enrollment: 26, capacity: 28, rating: 3.6, response_count: 21, cost_usd: 800 },
  { id: "S11", title: "Signage and Wayfinding",            week: 7, enrollment: 13, capacity: 22, rating: 3.4, response_count: 8,  cost_usd: 1050 },
  { id: "S12", title: "Research Synthesis Review",         week: 8, enrollment: 15, capacity: 30, rating: null, response_count: 0, cost_usd: 1150 }
].map(function (r) { return Object.freeze(r); }));

window.SESSION_DATA_META = Object.freeze({
  dataset: "synthetic-workshop-sessions",
  version: "1.0.0",
  synthetic: true,
  weeks: [1, 8],
  note: "Fictional demonstration data. Rating is a mean of 1–5 responses; response_count is the number of responses behind it."
});
