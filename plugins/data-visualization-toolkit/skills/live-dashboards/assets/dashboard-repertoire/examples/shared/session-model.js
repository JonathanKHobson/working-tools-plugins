/*
 * Shared derived-state model for the workbench and editorial alternatives.
 * Pure functions only: no DOM, no storage, no network. Plain classic script that
 * exposes window.SessionModel so both examples open from file://.
 *
 * Truth rules encoded here (see patterns.md, card P3 "scenario overlay"):
 *  - Source records are never mutated. A scenario is a separate {id: capacity} map.
 *  - Occupancy comparisons use integer arithmetic (enrollment*100 vs pct*capacity)
 *    so the 60% boundary is exact: S08 (15/25) is exactly 60% and not "below".
 *  - Pooled occupancy = sum(enrollment) / sum(capacity) over the rows in scope,
 *    never a mean of per-session percentages.
 *  - A null rating with response_count 0 means "no ratings yet", never 0.
 */
(function () {
  "use strict";

  var THRESHOLD_PCT = 60;
  var CAP_MIN = 1, CAP_MAX = 200;

  function validate(data) {
    if (!Array.isArray(data) || data.length === 0) return "The session data file did not load or is empty.";
    var seen = {};
    for (var i = 0; i < data.length; i++) {
      var r = data[i];
      if (!r || typeof r.id !== "string") return "Record " + (i + 1) + " has no id.";
      if (seen[r.id]) return "Duplicate session id " + r.id + ".";
      seen[r.id] = true;
      if (!(Number.isInteger(r.week) && r.week >= 1 && r.week <= 8)) return r.id + " has a week outside 1–8.";
      if (!(Number.isInteger(r.capacity) && r.capacity > 0)) return r.id + " has no valid capacity, so occupancy cannot be computed.";
      if (!(Number.isInteger(r.enrollment) && r.enrollment >= 0)) return r.id + " has an invalid enrollment.";
      if (r.rating !== null && !(r.rating >= 1 && r.rating <= 5)) return r.id + " has a rating outside 1–5.";
      if (r.rating === null && r.response_count !== 0) return r.id + " reports responses but no rating.";
      if (!(Number.isInteger(r.response_count) && r.response_count >= 0)) return r.id + " has an invalid response count.";
      if (r.rating !== null && r.response_count === 0) return r.id + " reports a rating without responses.";
    }
    return null;
  }

  function isBelow(enrollment, capacity) { return enrollment * 100 < THRESHOLD_PCT * capacity; }

  /* Returns derived rows: source fields untouched, plus effective (scenario) values. */
  function derive(data, scenario) {
    scenario = scenario || {};
    return data.map(function (r) {
      var hasScenario = Object.prototype.hasOwnProperty.call(scenario, r.id);
      var cap = hasScenario ? scenario[r.id] : r.capacity;
      return {
        src: r,
        id: r.id,
        occ: r.enrollment / r.capacity,
        below: isBelow(r.enrollment, r.capacity),
        scenario: hasScenario,
        effCapacity: cap,
        effOcc: r.enrollment / cap,
        effBelow: isBelow(r.enrollment, cap),
        costPerEnrolled: r.enrollment > 0 ? r.cost_usd / r.enrollment : null,
        noRatings: r.rating === null
      };
    });
  }

  /* Filter description is data, so the UI can attribute an empty result to a constraint. */
  function applyFilters(rows, f) {
    return rows.filter(function (d) {
      if (d.src.week < f.from || d.src.week > f.to) return false;
      if (f.belowOnly && !d.below) return false;
      return true;
    });
  }

  /* Which single constraint, if removed, would return rows? Used by empty states. */
  function explainEmpty(rows, f) {
    var inWeeks = rows.filter(function (d) { return d.src.week >= f.from && d.src.week <= f.to; });
    var out = { inWeekRange: inWeeks.length, belowAnywhere: rows.filter(function (d) { return d.below; }).length };
    if (inWeeks.length === 0) out.cause = "weeks";
    else if (f.belowOnly) out.cause = "below";
    else out.cause = "unknown";
    return out;
  }

  function pooled(rows, useScenario) {
    var e = 0, c = 0;
    rows.forEach(function (d) { e += d.src.enrollment; c += useScenario ? d.effCapacity : d.src.capacity; });
    return { enrollment: e, capacity: c, occ: c ? e / c : null };
  }

  /* Largest whole capacity at which occupancy is at least the threshold (goal inversion by arithmetic, not a model). */
  function capacityForThreshold(enrollment) {
    if (enrollment === 0) return null;
    return Math.floor(enrollment * 100 / THRESHOLD_PCT);
  }

  function validateCapacity(raw, record) {
    var s = String(raw).trim(), c = Number(s);
    if (s === "" || !Number.isInteger(c)) return { ok: false, msg: "Enter a whole number of seats." };
    if (c < CAP_MIN || c > CAP_MAX) return { ok: false, msg: "Capacity must be between " + CAP_MIN + " and " + CAP_MAX + " seats." };
    if (c < record.enrollment) return { ok: false, msg: "Capacity cannot be below current enrollment (" + record.enrollment + "). This scenario does not model removing enrolled participants." };
    return { ok: true, value: c };
  }

  /* Two-item comparison with explicit differences (B minus A), same units. */
  function compare(a, b) {
    return {
      occPoints: (b.effOcc - a.effOcc) * 100,
      enrolled: b.src.enrollment - a.src.enrollment,
      openSeats: (b.effCapacity - b.src.enrollment) - (a.effCapacity - a.src.enrollment),
      cost: b.src.cost_usd - a.src.cost_usd,
      costPerEnrolled: (a.costPerEnrolled != null && b.costPerEnrolled != null) ? b.costPerEnrolled - a.costPerEnrolled : null,
      ratingDifference: !a.noRatings && !b.noRatings ? b.src.rating - a.src.rating : null
    };
  }

  var fmt = {
    pct: function (x) { return x == null ? "—" : (x * 100).toFixed(1) + "%"; },
    pts: function (x) { var v = x.toFixed(1); return (x > 0 ? "+" : x < 0 ? "−" : "±") + v.replace("-", "") + " pts"; },
    signed: function (x) { return (x > 0 ? "+" : x < 0 ? "−" : "±") + Math.abs(x); },
    usd: function (x) { return "$" + Math.round(x).toLocaleString("en-US"); },
    usd2: function (x) { return x == null ? "n/a (0 enrolled)" : "$" + x.toFixed(2); },
    signedUsd: function (x) { return (x > 0 ? "+" : x < 0 ? "−" : "±") + "$" + Math.abs(Math.round(x)).toLocaleString("en-US"); },
    signedUsd2: function (x) { return x == null ? "—" : (x > 0 ? "+" : x < 0 ? "−" : "±") + "$" + Math.abs(x).toFixed(2); },
    rating: function (r) {
      if (r.rating === null) return "No ratings yet (0 responses)";
      return r.rating.toFixed(1) + " / 5 from " + r.response_count + (r.response_count === 1 ? " response" : " responses");
    },
    esc: function (s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
      });
    }
  };

  window.SessionModel = Object.freeze({
    THRESHOLD_PCT: THRESHOLD_PCT,
    CAP_MIN: CAP_MIN,
    CAP_MAX: CAP_MAX,
    validate: validate,
    isBelow: isBelow,
    derive: derive,
    applyFilters: applyFilters,
    explainEmpty: explainEmpty,
    pooled: pooled,
    capacityForThreshold: capacityForThreshold,
    validateCapacity: validateCapacity,
    compare: compare,
    fmt: fmt
  });
})();
