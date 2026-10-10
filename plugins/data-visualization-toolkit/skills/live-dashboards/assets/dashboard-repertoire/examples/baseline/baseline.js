/*
 * Baseline dashboard — generated from the installed skills listed in BASELINE-RECORD.md.
 * Plain script; no dependencies. Reads window.SESSION_DATA (shared, frozen) and never
 * mutates it. Scenario capacities are a separate overlay.
 */
(function () {
  "use strict";

  var THRESHOLD = 0.6;
  var LOW_N = 10; // below this many responses the rating is flagged as thin evidence
  var MAX_SELECTED = 2;

  var el = function (id) { return document.getElementById(id); };
  var fmtPct = function (x) { return (x * 100).toFixed(1) + "%"; };
  var fmtUsd = function (x) { return "$" + x.toLocaleString("en-US", { maximumFractionDigits: 0 }); };
  var fmtUsd2 = function (x) { return "$" + x.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };

  // ---------- data validation ----------
  function validate(data) {
    if (!Array.isArray(data) || data.length === 0) return "The session data file did not load or is empty.";
    for (var i = 0; i < data.length; i++) {
      var r = data[i];
      if (!r || typeof r.id !== "string") return "Record " + (i + 1) + " has no id.";
      if (!(r.week >= 1 && r.week <= 8)) return r.id + " has a week outside 1–8.";
      if (!(r.capacity > 0)) return r.id + " has no valid capacity, so occupancy cannot be computed.";
      if (!(r.enrollment >= 0)) return r.id + " has an invalid enrollment.";
      if (r.rating !== null && !(r.rating >= 1 && r.rating <= 5)) return r.id + " has a rating outside 1–5.";
      if (r.rating === null && r.response_count !== 0) return r.id + " has responses but no rating.";
    }
    return null;
  }

  var params = new URLSearchParams(location.search);
  var DATA = params.get("state") === "error" ? null : window.SESSION_DATA; // demo hook for the error state
  var problem = validate(DATA);

  var state = defaultState();

  function defaultState() {
    return { from: 1, to: 8, belowOnly: false, selected: [], scenario: {} };
  }

  function byId(id) {
    for (var i = 0; i < DATA.length; i++) if (DATA[i].id === id) return DATA[i];
    return null;
  }

  function capacityOf(r) { return state.scenario[r.id] != null ? state.scenario[r.id] : r.capacity; }
  function occ(r) { return r.enrollment / r.capacity; }          // source occupancy
  function occScenario(r) { return r.enrollment / capacityOf(r); } // with overlay

  function visibleRows() {
    return DATA.filter(function (r) {
      if (r.week < state.from || r.week > state.to) return false;
      if (state.belowOnly && !(occ(r) < THRESHOLD)) return false;
      return true;
    }).sort(function (a, b) { return occ(a) - occ(b) || a.week - b.week; });
  }

  // ---------- URL state ----------
  function readUrl() {
    var from = parseInt(params.get("from"), 10), to = parseInt(params.get("to"), 10);
    if (from >= 1 && from <= 8) state.from = from;
    if (to >= 1 && to <= 8) state.to = to;
    if (state.from > state.to) { var t = state.from; state.from = state.to; state.to = t; }
    state.belowOnly = params.get("below") === "1";
    var sel = (params.get("sel") || "").split(",").filter(function (id) { return byId(id); });
    state.selected = sel.slice(0, MAX_SELECTED);
    (params.get("sc") || "").split(",").forEach(function (pair) {
      var p = pair.split(":"), r = byId(p[0]), c = parseInt(p[1], 10);
      if (r && c >= r.enrollment && c >= 1 && c <= 200 && c !== r.capacity) state.scenario[r.id] = c;
    });
  }

  function writeUrl() {
    var q = new URLSearchParams();
    if (state.from !== 1) q.set("from", state.from);
    if (state.to !== 8) q.set("to", state.to);
    if (state.belowOnly) q.set("below", "1");
    if (state.selected.length) q.set("sel", state.selected.join(","));
    var sc = Object.keys(state.scenario).map(function (k) { return k + ":" + state.scenario[k]; });
    if (sc.length) q.set("sc", sc.join(","));
    var s = q.toString();
    try { history.replaceState(null, "", s ? "?" + s : location.pathname); } catch (e) { /* file:// in some browsers */ }
  }

  function announce(msg) { el("announcer").textContent = msg; }

  // ---------- render ----------
  function render() {
    var rows = visibleRows();
    renderScope(rows);
    renderChart(rows);
    renderCompare(rows);
    renderScenarioStatus();
    renderTable(rows);
    writeUrl();
  }

  function renderScope(rows) {
    var enr = 0, cap = 0;
    rows.forEach(function (r) { enr += r.enrollment; cap += r.capacity; });
    var parts = [
      "Showing <strong>" + rows.length + " of " + DATA.length + "</strong> sessions",
      "Weeks " + state.from + "–" + state.to
    ];
    if (state.belowOnly) parts.push("Below 60% only");
    if (rows.length) parts.push("Pooled occupancy " + fmtPct(enr / cap) + " (" + enr + "/" + cap + " seats)");
    var ns = Object.keys(state.scenario).length;
    if (ns) parts.push("<span class=\"tag tag-scenario\">Scenario active: " + ns + " hypothetical capacity</span>");
    el("scope-summary").innerHTML = parts.join(" · ");
  }

  function barSvg(r, selected) {
    var o = occ(r), pct = Math.min(o, 1) * 100;
    var cls = "fill" + (selected ? " selected" : o < THRESHOLD ? " below" : "");
    var inside = pct >= 70;
    var label = fmtPct(o) + (o < THRESHOLD ? " · below 60%" : "");
    var textX = inside ? (pct - 1) + "%" : (pct + 1) + "%";
    var s = '<svg class="bar-svg" aria-hidden="true" focusable="false">' +
      '<rect class="track" x="0" y="4" width="100%" height="20" rx="3"></rect>' +
      '<rect class="' + cls + '" x="0" y="4" width="' + pct + '%" height="20" rx="3"></rect>';
    if (state.scenario[r.id] != null) {
      var sp = Math.min(occScenario(r), 1) * 100;
      s += '<rect class="scenario-outline" x="0" y="2" width="' + sp + '%" height="24" rx="3"></rect>';
    }
    s += '<line class="ref" x1="60%" x2="60%" y1="0" y2="28"></line>' +
      '<text x="' + textX + '" y="19" text-anchor="' + (inside ? "end" : "start") + '"' +
      (inside ? ' style="fill:#fff"' : "") + '>' + label + '</text></svg>';
    return s;
  }

  function renderChart(rows) {
    var chart = el("chart"), empty = el("empty-state");
    if (!rows.length) {
      chart.innerHTML = "";
      empty.hidden = false;
      el("empty-detail").textContent = state.belowOnly
        ? "No session in weeks " + state.from + "–" + state.to + " is below 60% occupancy."
        : "No sessions are scheduled in weeks " + state.from + "–" + state.to + ".";
      el("empty-clear-below").hidden = !state.belowOnly;
      return;
    }
    empty.hidden = true;
    var html = rows.map(function (r) {
      var sel = state.selected.indexOf(r.id) !== -1;
      var desc = r.title + ", week " + r.week + ", occupancy " + fmtPct(occ(r)) + ", " + r.enrollment + " of " + r.capacity + " seats" +
        (occ(r) < THRESHOLD ? ", below 60 percent" : "") +
        (state.scenario[r.id] != null ? ", hypothetical capacity " + state.scenario[r.id] + " gives " + fmtPct(occScenario(r)) : "");
      return '<button type="button" class="bar-row" data-id="' + r.id + '" aria-pressed="' + sel + '" aria-label="' + esc(desc) + '">' +
        '<span class="bar-label">' + esc(r.title) + '<span class="meta">' + r.id + " · Week " + r.week + " · " + r.enrollment + "/" + r.capacity + " seats</span></span>" +
        barSvg(r, sel) + "</button>";
    }).join("");
    html += '<div class="axis-row" aria-hidden="true"><span></span><svg>' +
      [0, 25, 50, 75, 100].map(function (t) {
        return '<text x="' + t + '%" y="14" text-anchor="' + (t === 0 ? "start" : t === 100 ? "end" : "middle") + '">' + t + '%</text>';
      }).join("") + "</svg></div>";
    chart.innerHTML = html;
  }

  function ratingText(r) {
    if (r.rating === null) return "No ratings yet (0 responses)";
    var s = r.rating.toFixed(1) + " / 5 (n=" + r.response_count + ")";
    return r.response_count < LOW_N ? s + ' <span class="low-n">few responses</span>' : s;
  }

  function renderCompare(rows) {
    var box = el("compare");
    if (!state.selected.length) {
      box.innerHTML = '<p class="hint">Select two sessions in the chart to compare them on the same scales.</p>';
      return;
    }
    var visibleIds = rows.map(function (r) { return r.id; });
    var cards = state.selected.map(function (id) {
      var r = byId(id), o = occ(r), pct = Math.min(o, 1) * 100;
      var outside = visibleIds.indexOf(id) === -1;
      return '<div class="compare-card"><h3>' + esc(r.title) + "</h3>" +
        (outside ? '<p class="hint">Outside current filters — kept for comparison.</p>' : "") +
        '<svg class="mini" aria-hidden="true"><rect class="track" width="100%" height="14"></rect><rect class="fill" width="' + pct + '%" height="14"></rect><line class="ref" x1="60%" x2="60%" y1="0" y2="14"></line></svg>' +
        "<dl><dt>Occupancy</dt><dd>" + fmtPct(o) + "</dd>" +
        "<dt>Seats</dt><dd>" + r.enrollment + " / " + r.capacity + "</dd>" +
        "<dt>Week</dt><dd>" + r.week + "</dd>" +
        "<dt>Rating</dt><dd>" + ratingText(r) + "</dd>" +
        "<dt>Cost</dt><dd>" + fmtUsd(r.cost_usd) + "</dd>" +
        "<dt>Per enrolled</dt><dd>" + (r.enrollment ? fmtUsd2(r.cost_usd / r.enrollment) : "undefined (0 enrolled)") + "</dd></dl></div>";
    }).join("");
    var more = state.selected.length < MAX_SELECTED ? '<p class="hint">Select one more session to complete the comparison.</p>' : "";
    box.innerHTML = '<div class="compare-grid">' + cards + "</div>" + more +
      '<div class="state-actions" style="margin-top:10px"><button type="button" class="btn btn-quiet" id="clear-selection">Clear selection</button></div>';
    el("clear-selection").addEventListener("click", function () {
      state.selected = []; announce("Selection cleared."); render();
    });
  }

  function renderScenarioStatus() {
    var ids = Object.keys(state.scenario);
    if (!ids.length) { el("scenario-status").textContent = "No scenario applied. Showing source capacities."; return; }
    el("scenario-status").innerHTML = ids.map(function (id) {
      var r = byId(id);
      return "<strong>Hypothetical:</strong> " + esc(r.title) + " capacity " + r.capacity + " → " + state.scenario[id] +
        ", occupancy " + fmtPct(occ(r)) + " → " + fmtPct(occScenario(r)) + " (enrollment held at " + r.enrollment + ")";
    }).join("<br>");
  }

  function renderTable(rows) {
    var head = "<thead><tr><th scope=\"col\">ID</th><th scope=\"col\">Session</th><th scope=\"col\">Week</th><th scope=\"col\">Enrolled</th><th scope=\"col\">Capacity</th><th scope=\"col\">Occupancy</th><th scope=\"col\">Rating (1–5)</th><th scope=\"col\">Responses</th><th scope=\"col\">Cost</th><th scope=\"col\">Status</th></tr></thead>";
    if (!rows.length) {
      el("data-table").innerHTML = head + '<tbody><tr><td colspan="10">No sessions in the current view.</td></tr></tbody>';
      return;
    }
    var body = rows.map(function (r) {
      var sc = state.scenario[r.id] != null;
      var tags = [];
      if (occ(r) < THRESHOLD) tags.push('<span class="tag tag-below">Below 60%</span>');
      if (sc) tags.push('<span class="tag tag-scenario">Scenario: cap ' + state.scenario[r.id] + " → " + fmtPct(occScenario(r)) + "</span>");
      return '<tr class="' + (state.selected.indexOf(r.id) !== -1 ? "is-selected" : "") + '">' +
        "<td>" + r.id + "</td><td>" + esc(r.title) + "</td><td>" + r.week + "</td><td>" + r.enrollment + "</td><td>" + r.capacity +
        "</td><td>" + fmtPct(occ(r)) + "</td><td>" + (r.rating === null ? "—" : r.rating.toFixed(1)) + "</td><td>" + r.response_count +
        "</td><td>" + fmtUsd(r.cost_usd) + "</td><td>" + tags.join(" ") + "</td></tr>";
    }).join("");
    el("data-table").innerHTML = head + "<tbody>" + body + "</tbody>";
  }

  // ---------- interactions ----------
  function toggleSelect(id) {
    var i = state.selected.indexOf(id);
    if (i !== -1) { state.selected.splice(i, 1); announce(byId(id).title + " removed from comparison."); }
    else {
      if (state.selected.length >= MAX_SELECTED) {
        var dropped = state.selected.shift();
        announce(byId(dropped).title + " replaced by " + byId(id).title + ".");
      } else announce(byId(id).title + " added to comparison.");
      state.selected.push(id);
    }
    render();
    var btn = document.querySelector('.bar-row[data-id="' + id + '"]');
    if (btn) btn.focus();
  }

  function fillWeekSelects() {
    var opts = "";
    for (var w = 1; w <= 8; w++) opts += '<option value="' + w + '">Week ' + w + "</option>";
    el("week-from").innerHTML = opts; el("week-to").innerHTML = opts;
  }

  function syncControls() {
    el("week-from").value = state.from; el("week-to").value = state.to;
    el("below-only").checked = state.belowOnly;
  }

  function fillScenarioSelect() {
    el("scenario-session").innerHTML = DATA.map(function (r) {
      return '<option value="' + r.id + '">' + r.id + " · " + esc(r.title) + "</option>";
    }).join("");
    syncScenarioInput();
  }
  function syncScenarioInput() {
    var r = byId(el("scenario-session").value);
    el("scenario-capacity").value = capacityOf(r);
    el("scenario-error").textContent = "";
  }

  function bind() {
    el("week-from").addEventListener("change", function () {
      state.from = +this.value; if (state.from > state.to) { state.to = state.from; }
      syncControls(); render();
    });
    el("week-to").addEventListener("change", function () {
      state.to = +this.value; if (state.to < state.from) { state.from = state.to; }
      syncControls(); render();
    });
    el("below-only").addEventListener("change", function () { state.belowOnly = this.checked; render(); });

    el("chart").addEventListener("click", function (e) {
      var b = e.target.closest(".bar-row"); if (b) toggleSelect(b.getAttribute("data-id"));
    });
    el("chart").addEventListener("keydown", function (e) {
      if (e.key === "Escape" && state.selected.length) { state.selected = []; announce("Selection cleared."); render(); }
    });

    function resetAll() {
      state = defaultState(); syncControls(); syncScenarioInput();
      announce("View reset: all weeks, all sessions, no selection, source capacities.");
      render(); el("chart-heading").focus();
    }
    el("reset-all").addEventListener("click", resetAll);
    el("empty-reset").addEventListener("click", resetAll);
    el("empty-clear-below").addEventListener("click", function () {
      state.belowOnly = false; syncControls(); render(); announce("Showing all occupancy levels."); el("chart-heading").focus();
    });

    el("scenario-session").addEventListener("change", syncScenarioInput);
    el("scenario-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var r = byId(el("scenario-session").value);
      var raw = el("scenario-capacity").value.trim(), c = Number(raw);
      var err = "";
      if (raw === "" || !Number.isInteger(c)) err = "Enter a whole number of seats.";
      else if (c < 1 || c > 200) err = "Capacity must be between 1 and 200 seats.";
      else if (c < r.enrollment) err = "Capacity cannot be below current enrollment (" + r.enrollment + "). This scenario does not model removing enrolled participants.";
      el("scenario-error").textContent = err;
      el("scenario-capacity").setAttribute("aria-invalid", err ? "true" : "false");
      if (err) { el("scenario-capacity").focus(); return; }
      if (c === r.capacity) delete state.scenario[r.id]; else state.scenario[r.id] = c;
      announce("Hypothetical capacity applied to " + r.title + ".");
      render();
    });
    el("scenario-restore").addEventListener("click", function () {
      var r = byId(el("scenario-session").value);
      delete state.scenario[r.id]; syncScenarioInput();
      announce("Restored source capacity for " + r.title + ": " + r.capacity + " seats.");
      render();
    });
  }

  // ---------- boot ----------
  if (problem) {
    el("error-state").hidden = false;
    el("error-state").innerHTML = "<p><strong>The dashboard cannot show sessions.</strong> " + esc(problem) +
      " No values are displayed rather than showing partial or guessed figures.</p><p><a href=\"index.html\">Reload with the bundled data</a></p>";
    el("scope-summary").textContent = "Data unavailable.";
    ["controls", "table-panel"].forEach(function (c) { document.querySelector("." + c).hidden = true; });
    document.querySelector(".side").hidden = true;
    el("reset-all").hidden = true;
    return;
  }
  fillWeekSelects();
  readUrl();
  syncControls();
  fillScenarioSelect();
  bind();
  render();
})();
