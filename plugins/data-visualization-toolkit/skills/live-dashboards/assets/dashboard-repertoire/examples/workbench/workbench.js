/*
 * Workbench alternative. Sequence: scope (brush weeks) → locate (plot/ledger) →
 * pin A/B → compare with explicit differences → test a hypothetical capacity.
 * Mechanisms: constraint chips with provenance, focus+context plot, A/B slots with
 * explicit replace, superposed comparison + difference column, scenario overlay
 * ledger with goal inversion, undo history, constraint-attributed empty state.
 * Depends on ../shared/sessions-data.js and ../shared/session-model.js (classic scripts).
 */
(function () {
  "use strict";
  var M = window.SessionModel, F = M.fmt;
  var $ = function (id) { return document.getElementById(id); };
  var params = new URLSearchParams(location.search);
  var DATA = params.get("state") === "error" ? null : window.SESSION_DATA;
  var problem = M.validate(DATA);

  // ---------- state ----------
  var state = initialState();
  var ui = { cursor: null, pendingReplace: null, scTarget: null, sort: { key: "week", dir: "asc" }, brush: null };
  var undoStack = [];
  var HISTORY_MAX = 50;

  function initialState() { return { from: 1, to: 8, belowOnly: false, pins: [null, null], scenario: {} }; }
  function snapshot() { return JSON.stringify(state); }
  function byId(id) { for (var i = 0; i < DATA.length; i++) if (DATA[i].id === id) return DATA[i]; return null; }
  function announce(msg) { $("announcer").textContent = ""; setTimeout(function () { $("announcer").textContent = msg; }, 30); }

  /* Every committed change is undoable. Transient UI (cursor, brush preview) is not. */
  function commit(mutate, message) {
    var before = snapshot();
    mutate();
    if (snapshot() === before) return;
    undoStack.push(before);
    if (undoStack.length > HISTORY_MAX) undoStack.shift();
    render();
    if (message) announce(message);
  }
  function undo() {
    if (!undoStack.length) return;
    state = JSON.parse(undoStack.pop());
    ui.pendingReplace = null;
    syncControls();
    render();
    announce("Undone. " + describeScope());
  }

  // ---------- derived ----------
  function all() { return M.derive(DATA, state.scenario); }
  function visible(rows) { return M.applyFilters(rows, state); }
  function describeScope() {
    var v = visible(all());
    return v.length + " of " + DATA.length + " sessions in scope, weeks " + state.from + "–" + state.to + (state.belowOnly ? ", below 60% only" : "") + ".";
  }

  // ---------- URL (commit-level state only) ----------
  function readUrl() {
    var f = parseInt(params.get("from"), 10), t = parseInt(params.get("to"), 10);
    if (f >= 1 && f <= 8) state.from = f;
    if (t >= 1 && t <= 8) state.to = t;
    if (state.from > state.to) { var x = state.from; state.from = state.to; state.to = x; }
    state.belowOnly = params.get("below") === "1";
    ["a", "b"].forEach(function (k, i) { var id = params.get(k); if (id && byId(id) && state.pins.indexOf(id) === -1) state.pins[i] = id; });
    (params.get("sc") || "").split(",").forEach(function (p) {
      var kv = p.split(":"), r = byId(kv[0]); if (!r) return;
      var v = M.validateCapacity(kv[1], r); if (v.ok && v.value !== r.capacity) state.scenario[r.id] = v.value;
    });
  }
  function writeUrl() {
    var q = new URLSearchParams();
    if (state.from !== 1) q.set("from", state.from);
    if (state.to !== 8) q.set("to", state.to);
    if (state.belowOnly) q.set("below", "1");
    if (state.pins[0]) q.set("a", state.pins[0]);
    if (state.pins[1]) q.set("b", state.pins[1]);
    var sc = Object.keys(state.scenario).map(function (k) { return k + ":" + state.scenario[k]; });
    if (sc.length) q.set("sc", sc.join(","));
    var s = q.toString();
    try { window.history.replaceState(null, "", s ? "?" + s : location.pathname); } catch (e) { /* some browsers block on file:// */ }
  }

  // ---------- render ----------
  function render() {
    var rows = all(), vis = visible(rows);
    renderCommand(rows, vis);
    renderPlot(rows, vis);
    renderTray(rows);
    renderScenario(rows);
    renderLedger(vis, rows);
    renderMini(rows);
    $("undo").disabled = undoStack.length === 0;
    writeUrl();
  }

  function renderCommand(rows, vis) {
    var p = M.pooled(vis, false);
    var text = vis.length + " of " + DATA.length + " sessions";
    if (vis.length) text += " · pooled " + F.pct(p.occ) + " (" + p.enrollment + "/" + p.capacity + " seats)";
    var hasSc = vis.some(function (d) { return d.scenario; });
    if (hasSc) { var ps = M.pooled(vis, true); text += " · with scenario " + F.pct(ps.occ); }
    $("scope-count").textContent = text;

    var chips = [];
    if (state.from !== 1 || state.to !== 8) chips.push('<li class="chip">Weeks ' + state.from + "–" + state.to + ' <button type="button" data-action="clear-weeks" aria-label="Remove week range, show all weeks">×</button></li>');
    if (state.belowOnly) chips.push('<li class="chip">Below 60% only <button type="button" data-action="clear-below" aria-label="Remove below 60% constraint">×</button></li>');
    var nsc = Object.keys(state.scenario).length;
    if (nsc) chips.push('<li class="chip scenario">Scenario: ' + nsc + " capacity change" + (nsc > 1 ? "s" : "") + ' <button type="button" data-action="goto-scenario" aria-label="Go to scenario controls">→</button></li>');
    if (!chips.length) chips.push('<li class="chip default">All weeks · all occupancy levels · source capacities</li>');
    $("scope-chips").innerHTML = chips.join("");
  }

  // Stable positions from the full dataset so marks never jump when filters change.
  function slotOf(r) {
    var same = DATA.filter(function (d) { return d.week === r.week; });
    return { i: same.indexOf(r), n: same.length };
  }

  var geom = null;
  function renderPlot(rows, vis) {
    var svg = $("plot");
    var box = svg.getBoundingClientRect();
    var W = Math.round(box.width) || 700, H = Math.round(box.height) || 320;
    var ml = 40, mr = 14, mt = 14, mb = 46;
    var pw = W - ml - mr, ph = H - mt - mb, bw = pw / 8;
    var y = function (o) { return mt + (1 - Math.min(o, 1)) * ph; };
    var xw = function (w) { return ml + (w - 1) * bw; };
    geom = { ml: ml, bw: bw, mt: mt, ph: ph, H: H, W: W, axisTop: mt + ph + 4 };
    var visIds = vis.map(function (d) { return d.id; });
    var s = '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#6b3fa0"/></marker></defs>';
    s += '<rect class="band-below" x="' + ml + '" y="' + y(0.6) + '" width="' + pw + '" height="' + (y(0) - y(0.6)) + '"/>';
    [0, 0.25, 0.5, 0.75, 1].forEach(function (t) {
      s += '<line class="grid" x1="' + ml + '" x2="' + (ml + pw) + '" y1="' + y(t) + '" y2="' + y(t) + '"/>';
      s += '<text x="' + (ml - 6) + '" y="' + (y(t) + 4) + '" text-anchor="end">' + t * 100 + "%</text>";
    });
    s += '<line class="threshold" x1="' + ml + '" x2="' + (ml + pw) + '" y1="' + y(0.6) + '" y2="' + y(0.6) + '"/>';
    s += '<text x="' + (ml + pw) + '" y="' + (y(0.6) - 5) + '" text-anchor="end" style="fill:#b8420f">60% threshold</text>';
    for (var w = 1; w <= 8; w++) {
      var out = w < state.from || w > state.to;
      if (out) s += '<rect class="out-of-scope" x="' + xw(w) + '" y="' + mt + '" width="' + bw + '" height="' + (ph + mb - 8) + '" opacity="0.75"/>';
      s += '<text class="week-label" x="' + (xw(w) + bw / 2) + '" y="' + (mt + ph + 22) + '" text-anchor="middle"' + (out ? ' opacity="0.45"' : "") + ">W" + w + "</text>";
    }
    s += '<line class="scope-edge" x1="' + xw(state.from) + '" x2="' + xw(state.from) + '" y1="' + mt + '" y2="' + (mt + ph + 30) + '"/>';
    s += '<line class="scope-edge" x1="' + xw(state.to + 1) + '" x2="' + xw(state.to + 1) + '" y1="' + mt + '" y2="' + (mt + ph + 30) + '"/>';
    if (ui.brush) {
      var a = Math.min(ui.brush.a, ui.brush.b), b = Math.max(ui.brush.a, ui.brush.b);
      s += '<rect class="brush-preview" x="' + xw(a) + '" y="' + mt + '" width="' + (xw(b + 1) - xw(a)) + '" height="' + (ph + 30) + '"/>';
    }
    s += '<text x="' + ml + '" y="' + (H - 4) + '">Drag here to set week range ↔</text>';
    s += '<rect class="axis-hit" id="axis-hit" x="' + ml + '" y="' + (mt + ph + 2) + '" width="' + pw + '" height="' + (mb - 6) + '"/>';

    rows.forEach(function (d) {
      var sl = slotOf(d.src);
      var cx = xw(d.src.week) + bw * (sl.i + 1) / (sl.n + 1), cy = y(d.occ);
      var inScope = visIds.indexOf(d.id) !== -1;
      var pinIdx = state.pins.indexOf(d.id);
      if (d.scenario) {
        var gy = y(d.effOcc);
        if (Math.abs(gy - cy) > 12) s += '<line class="ghost-link" x1="' + cx + '" y1="' + (cy + (gy < cy ? -9 : 9)) + '" x2="' + cx + '" y2="' + (gy + (gy < cy ? 10 : -10)) + '"' + (inScope ? "" : ' opacity="0.3"') + "/>";
        s += '<circle class="ghost" cx="' + cx + '" cy="' + gy + '" r="7"' + (inScope ? "" : ' opacity="0.3"') + "/>";
      }
      s += '<g data-id="' + d.id + '"' + (inScope ? "" : ' data-faded="1"') + ">";
      s += '<circle cx="' + cx + '" cy="' + cy + '" r="14" fill="transparent"/>';
      s += '<circle class="dot ' + (d.below ? "below" : "ok") + (inScope ? "" : " faded") + '" cx="' + cx + '" cy="' + cy + '" r="7"><title>' + F.esc(d.src.title) + " · " + F.pct(d.occ) + "</title></circle></g>";
      s += '<text class="dot-label' + (inScope ? "" : " faded") + '" x="' + (cx + 10) + '" y="' + (cy + 4) + '">' + d.id + "</text>";
      if (pinIdx !== -1) {
        s += '<circle class="pin-ring' + (pinIdx === 1 ? " b" : "") + '" cx="' + cx + '" cy="' + cy + '" r="11"/>';
        s += '<rect class="pin-tag-bg" x="' + (cx - 7) + '" y="' + (cy - 28) + '" width="14" height="14" rx="2"/><text class="pin-tag" x="' + cx + '" y="' + (cy - 17) + '" text-anchor="middle">' + (pinIdx ? "B" : "A") + "</text>";
      }
      if (ui.cursor === d.id) s += '<circle class="cursor" cx="' + cx + '" cy="' + cy + '" r="15"/>';
    });
    svg.innerHTML = s;

    var below = vis.filter(function (d) { return d.below; });
    $("plot-summary").textContent = vis.length
      ? vis.length + " sessions in scope. " + below.length + " below 60% occupancy" + (below.length ? ": " + below.map(function (d) { return d.id + " " + F.pct(d.occ); }).join(", ") : "") + ". Full values are in the session ledger."
      : "No sessions in scope.";
    var empty = $("plot-empty");
    if (!vis.length) { empty.hidden = false; empty.innerHTML = emptyHtml(rows); } else { empty.hidden = true; empty.innerHTML = ""; }
  }

  function emptyHtml(rows) {
    var why = M.explainEmpty(rows, state);
    var msg, actions = "";
    if (why.cause === "below") {
      msg = "Weeks " + state.from + "–" + state.to + " contain " + why.inWeekRange + " session" + (why.inWeekRange === 1 ? "" : "s") + ", but none is below 60% occupied.";
      actions = '<button type="button" class="tool" data-action="clear-below">Remove “below 60%”</button> <button type="button" class="tool" data-action="clear-weeks">Widen to all weeks (' + why.belowAnywhere + " below 60%)</button>";
    } else {
      msg = "No sessions are scheduled in weeks " + state.from + "–" + state.to + ".";
      actions = '<button type="button" class="tool" data-action="clear-weeks">Widen to all weeks</button>';
    }
    return "<p><strong>Nothing in scope.</strong> " + msg + "</p><div class=\"row-actions\">" + actions + ' <button type="button" class="tool" data-action="undo">Undo last change</button></div>';
  }

  function slotHtml(d, idx, visIds) {
    var tag = idx ? "B" : "A";
    if (!d) return '<div class="slot empty-slot' + (idx ? " b" : "") + '"><span class="tag">' + tag + "</span> empty — pin a session</div>";
    var outside = visIds.indexOf(d.id) === -1;
    return '<div class="slot' + (idx ? " b" : "") + '"><h3><span class="tag">' + tag + "</span>" + F.esc(d.src.title) + "</h3>" +
      '<div style="font-family:var(--mono);font-size:0.8rem">' + d.id + " · W" + d.src.week + " · " + F.pct(d.effOcc) + (d.scenario ? " (hyp.)" : "") + "</div>" +
      (outside ? '<div class="hint">Outside current scope — kept pinned.</div>' : "") +
      '<button type="button" class="unpin" data-action="unpin" data-id="' + d.id + '">Unpin ' + tag + "</button></div>";
  }

  function renderTray(rows) {
    var find = function (id) { return rows.filter(function (d) { return d.id === id; })[0] || null; };
    var A = find(state.pins[0]), B = find(state.pins[1]);
    var visIds = visible(rows).map(function (d) { return d.id; });
    var h = '<div class="slots">' + slotHtml(A, 0, visIds) + slotHtml(B, 1, visIds) + "</div>";
    if (ui.pendingReplace) {
      var p = byId(ui.pendingReplace);
      h += '<div class="replace-prompt" id="replace-prompt"><p>A and B are both pinned. Where should <strong>' + F.esc(p.title) + "</strong> go?</p>" +
        '<div class="row-actions"><button type="button" class="tool" data-action="replace" data-slot="0">Replace A</button><button type="button" class="tool" data-action="replace" data-slot="1">Replace B</button><button type="button" class="tool" data-action="cancel-replace">Cancel</button></div></div>';
    }
    if (A && B) {
      var c = M.compare(A, B);
      var anySc = A.scenario || B.scenario;
      h += superposeSvg(A, B);
      var ratingCell = function (d) { return d.noRatings ? "none yet (n=0)" : d.src.rating.toFixed(1) + " / 5 (n=" + d.src.response_count + ")"; };
      var ratingDelta = c.ratingDifference === null ? "—" : (c.ratingDifference >= 0 ? "+" : "−") + Math.abs(c.ratingDifference).toFixed(1) + " / 5";
      var ratingNote = c.ratingDifference === null ? "No rating difference: at least one session has no responses." :
        "Descriptive difference of recorded means only. Response counts differ; sampling and comparability are unknown. This is not a significance test.";
      h += '<table class="diff"><caption class="visually-hidden">Comparison of A and B with B minus A differences</caption><thead><tr><th scope="col"></th><th scope="col">A ' + A.id + '</th><th scope="col">B ' + B.id + '</th><th scope="col">B − A</th></tr></thead><tbody>' +
        row("Occupancy" + (anySc ? "*" : ""), F.pct(A.effOcc), F.pct(B.effOcc), F.pts(c.occPoints)) +
        row("Enrolled", A.src.enrollment, B.src.enrollment, F.signed(c.enrolled)) +
        row("Capacity" + (anySc ? "*" : ""), A.effCapacity, B.effCapacity, F.signed(B.effCapacity - A.effCapacity)) +
        row("Open seats" + (anySc ? "*" : ""), A.effCapacity - A.src.enrollment, B.effCapacity - B.src.enrollment, F.signed(c.openSeats)) +
        row("Cost", F.usd(A.src.cost_usd), F.usd(B.src.cost_usd), F.signedUsd(c.cost)) +
        row("Cost / enrolled", F.usd2(A.costPerEnrolled), F.usd2(B.costPerEnrolled), F.signedUsd2(c.costPerEnrolled)) +
        row("Rating", ratingCell(A), ratingCell(B), ratingDelta) +
        '<tr><td class="note" colspan="4">' + ratingNote + (anySc ? " Asterisked capacity and occupancy rows include hypothetical values; ratings do not." : "") + "</td></tr></tbody></table>";
    } else if (A || B) {
      h += '<p class="hint">Pin one more session to see differences.</p>';
    } else {
      h += '<p class="hint">Pin two sessions from the plot or the ledger’s Pin column. Both use the same 0–100% scale.</p>';
    }
    $("tray-body").innerHTML = h;
    function row(label, a, b, d) { return '<tr><th scope="row">' + label + "</th><td>" + a + "</td><td>" + b + '</td><td class="delta">' + d + "</td></tr>"; }
  }

  // Superposition on one shared track (Gleicher et al.): both bars read against the same 0–100% scale.
  function superposeSvg(A, B) {
    var w = 300, x0 = 26, x1 = w - 8, sx = function (o) { return x0 + Math.min(o, 1) * (x1 - x0); };
    return '<svg class="superpose" viewBox="0 0 ' + w + ' 58" role="img" aria-label="A ' + F.pct(A.effOcc) + ", B " + F.pct(B.effOcc) + ' on a shared 0 to 100 percent scale">' +
      '<rect x="' + x0 + '" y="6" width="' + (x1 - x0) + '" height="32" fill="#e4e4de"/>' +
      '<rect x="' + x0 + '" y="8" width="' + (sx(A.effOcc) - x0) + '" height="12" fill="#1d2327"/>' +
      '<rect x="' + x0 + '" y="24" width="' + (sx(B.effOcc) - x0) + '" height="12" fill="#fbfaf7" stroke="#1d2327" stroke-dasharray="3 2"/>' +
      '<line x1="' + sx(0.6) + '" x2="' + sx(0.6) + '" y1="2" y2="42" stroke="#b8420f" stroke-dasharray="3 2"/>' +
      '<text x="4" y="18">A</text><text x="4" y="34">B</text>' +
      '<text x="' + x0 + '" y="54">0%</text><text x="' + sx(0.6) + '" y="54" text-anchor="middle">60%</text><text x="' + x1 + '" y="54" text-anchor="end">100%</text></svg>';
  }

  function renderScenario(rows) {
    var sel = $("sc-session");
    if (!ui.scTarget) ui.scTarget = state.pins[0] || "S04";
    sel.value = ui.scTarget;
    var r = byId(ui.scTarget), d = rows.filter(function (x) { return x.id === r.id; })[0];
    if (document.activeElement !== $("sc-cap")) $("sc-cap").value = d.effCapacity;
    previewScenario();
    var goal = M.capacityForThreshold(r.enrollment);
    var gb = $("sc-goal");
    if (goal == null) { gb.hidden = true; } else {
      goal = Math.min(goal, M.CAP_MAX);
      gb.hidden = false;
      gb.textContent = "Try " + goal + " seats (largest capacity ≥60% full)";
      gb.setAttribute("data-goal", goal);
    }
    var ids = Object.keys(state.scenario);
    if (!ids.length) { $("sc-ledger").innerHTML = '<p class="hint">No hypothetical changes. All values are source values.</p>'; return; }
    $("sc-ledger").innerHTML = '<ul class="sc-list" aria-label="Active hypothetical changes">' + ids.map(function (id) {
      var s = byId(id), dd = rows.filter(function (x) { return x.id === id; })[0];
      return "<li><span>" + id + " cap " + s.capacity + "→" + state.scenario[id] + " · " + F.pct(dd.occ) + "→" + F.pct(dd.effOcc) + '</span><button type="button" class="tool" data-action="restore" data-id="' + id + '">Restore ' + id + "</button></li>";
    }).join("") + '</ul><div class="row-actions"><button type="button" class="tool" data-action="restore-all">Restore all source capacities</button></div>';
  }

  function previewScenario() {
    var r = byId($("sc-session").value), v = M.validateCapacity($("sc-cap").value, r);
    $("sc-error").textContent = v.ok ? "" : v.msg;
    $("sc-cap").setAttribute("aria-invalid", v.ok ? "false" : "true");
    $("sc-preview").textContent = v.ok
      ? "Source " + r.enrollment + "/" + r.capacity + " = " + F.pct(r.enrollment / r.capacity) + " → hypothetical " + r.enrollment + "/" + v.value + " = " + F.pct(r.enrollment / v.value)
      : "";
  }

  var SORTS = {
    week: function (d) { return d.src.week * 100 + parseInt(d.id.slice(1), 10); },
    occ: function (d) { return d.occ; },
    rating: function (d) { return d.noRatings ? null : d.src.rating; },
    cost: function (d) { return d.src.cost_usd; },
    cpe: function (d) { return d.costPerEnrolled; }
  };

  function renderLedger(vis, rows) {
    var key = ui.sort.key, dir = ui.sort.dir === "asc" ? 1 : -1;
    var sorted = vis.slice().sort(function (a, b) {
      var va = SORTS[key](a), vb = SORTS[key](b);
      if (va === null && vb === null) return 0;
      if (va === null) return 1; if (vb === null) return -1; // missing always last
      return (va - vb) * dir || (SORTS.week(a) - SORTS.week(b));
    });
    var th = function (k, label, extra) {
      var s = ui.sort.key === k ? (ui.sort.dir === "asc" ? "ascending" : "descending") : "none";
      return '<th scope="col" aria-sort="' + s + '"' + (extra || "") + '><button type="button" class="sort" data-sort="' + k + '">' + label + "</button></th>";
    };
    var head = '<thead><tr><th scope="col" class="l">Pin</th><th scope="col" class="l">Session</th>' + th("week", "Wk") + th("occ", "Occupancy (source)") +
      '<th scope="col">Seats</th>' + th("rating", "Rating (n)") + th("cost", "Cost") + th("cpe", "Cost / enrolled") + '<th scope="col" class="l">Hypothetical</th></tr></thead>';
    var body;
    if (!sorted.length) {
      body = '<tbody><tr><td colspan="9" class="l">' + emptyHtml(rows) + "</td></tr></tbody>";
    } else {
      body = "<tbody>" + sorted.map(function (d) {
        var pinIdx = state.pins.indexOf(d.id), pinned = pinIdx !== -1;
        var pct = Math.min(d.occ, 1) * 100;
        return '<tr class="' + (pinned ? "pinned" : "") + '"><td class="l"><button type="button" class="pin-btn" data-action="pin" data-id="' + d.id + '" aria-pressed="' + pinned + '" aria-label="' + (pinned ? "Unpin " : "Pin ") + F.esc(d.src.title) + '">' + (pinned ? (pinIdx ? "B" : "A") : "Pin") + "</button></td>" +
          '<td class="l"><strong>' + d.id + "</strong> " + F.esc(d.src.title) + "</td>" +
          "<td>" + d.src.week + "</td>" +
          '<td><span class="cellbar" aria-hidden="true"><i class="' + (d.below ? "below" : "") + '" style="width:' + pct + '%"></i><b></b></span>' + F.pct(d.occ) + (d.below ? ' <span class="status-below">below 60%</span>' : "") + "</td>" +
          "<td>" + d.src.enrollment + "/" + d.src.capacity + "</td>" +
          "<td>" + (d.noRatings ? '<span class="thin">none yet (n=0)</span>' : d.src.rating.toFixed(1) + " (n=" + d.src.response_count + ")") + "</td>" +
          "<td>" + F.usd(d.src.cost_usd) + "</td><td>" + F.usd2(d.costPerEnrolled) + "</td>" +
          '<td class="l sc-cell">' + (d.scenario ? "cap " + d.effCapacity + " → " + F.pct(d.effOcc) : "") + "</td></tr>";
      }).join("") + "</tbody>";
    }
    $("ledger").innerHTML = head + body;
    var labels = { week: "week", occ: "occupancy", rating: "rating", cost: "cost", cpe: "cost per enrolled" };
    $("ledger-note").textContent = sorted.length + " in scope · sorted by " + labels[key] + (ui.sort.dir === "asc" ? " ↑" : " ↓") + " · occupancy uses source capacity; hypothetical values have their own column.";
  }

  function renderMini(rows) {
    var mini = $("tray-mini");
    var A = rows.filter(function (d) { return d.id === state.pins[0]; })[0], B = rows.filter(function (d) { return d.id === state.pins[1]; })[0];
    if (!A && !B) { mini.hidden = true; document.body.classList.remove("has-mini"); return; }
    mini.hidden = false; document.body.classList.add("has-mini");
    var t = (A ? "A " + A.id + " " + F.pct(A.effOcc) : "A —") + " · " + (B ? "B " + B.id + " " + F.pct(B.effOcc) : "B —");
    if (A && B) t += " · Δ " + F.pts((B.effOcc - A.effOcc) * 100);
    $("tray-mini-text").textContent = t;
  }

  // ---------- actions ----------
  function togglePin(id) {
    var idx = state.pins.indexOf(id), r = byId(id);
    if (idx !== -1) { commit(function () { state.pins[idx] = null; }, r.title + " unpinned from " + (idx ? "B" : "A") + "."); return; }
    var free = state.pins.indexOf(null);
    if (free !== -1) { commit(function () { state.pins[free] = id; }, r.title + " pinned as " + (free ? "B" : "A") + "."); return; }
    ui.pendingReplace = id; render();
    var first = document.querySelector('#replace-prompt button'); if (first) first.focus();
    announce("A and B are both pinned. Choose which to replace, or cancel.");
  }

  function setRange(a, b, msg) {
    commit(function () { state.from = Math.min(a, b); state.to = Math.max(a, b); }, msg || ("Weeks " + Math.min(a, b) + "–" + Math.max(a, b) + ". "));
    syncControls();
    announce(describeScope());
  }

  function applyScenarioValue(r, value) {
    commit(function () {
      if (value === r.capacity) delete state.scenario[r.id]; else state.scenario[r.id] = value;
    }, "Hypothetical capacity for " + r.id + ": " + value + " seats, occupancy " + F.pct(r.enrollment / value) + ". Source unchanged.");
  }

  function onAction(e) {
    var t = e.target.closest("[data-action]"); if (!t) return;
    var a = t.getAttribute("data-action"), id = t.getAttribute("data-id");
    if (a === "pin") {
      togglePin(id);
      if (!ui.pendingReplace) { var again = document.querySelector('.pin-btn[data-id="' + id + '"]'); if (again) again.focus(); }
    }
    else if (a === "unpin") { togglePin(id); $("tray").focus(); }
    else if (a === "replace") {
      var slot = +t.getAttribute("data-slot"), nid = ui.pendingReplace; ui.pendingReplace = null;
      commit(function () { state.pins[slot] = nid; }, byId(nid).title + " replaced " + (slot ? "B" : "A") + ".");
      $("tray").focus();
    } else if (a === "cancel-replace") { ui.pendingReplace = null; render(); announce("Kept current A and B."); $("tray").focus(); }
    else if (a === "clear-weeks") { commit(function () { state.from = 1; state.to = 8; }); syncControls(); announce("All weeks. " + describeScope()); $("ledger-heading").focus(); }
    else if (a === "clear-below") { commit(function () { state.belowOnly = false; }); syncControls(); announce("All occupancy levels. " + describeScope()); $("ledger-heading").focus(); }
    else if (a === "goto-scenario") { $("scenario").focus(); $("scenario").scrollIntoView({ block: "start" }); }
    else if (a === "restore") { var r = byId(id); commit(function () { delete state.scenario[id]; }, "Restored source capacity for " + id + ": " + r.capacity + " seats."); }
    else if (a === "restore-all") { commit(function () { state.scenario = {}; }, "All source capacities restored."); }
    else if (a === "undo") undo();
  }

  // ---------- plot pointer + keyboard ----------
  function weekAt(clientX) {
    var rect = $("plot").getBoundingClientRect();
    var w = Math.floor((clientX - rect.left - geom.ml) / geom.bw) + 1;
    return Math.max(1, Math.min(8, w));
  }
  function bindPlot() {
    var svg = $("plot");
    svg.addEventListener("pointerdown", function (e) {
      if (!e.target || e.target.id !== "axis-hit") return;
      e.preventDefault();
      svg.setPointerCapture(e.pointerId);
      ui.brush = { a: weekAt(e.clientX), b: weekAt(e.clientX), id: e.pointerId };
      renderPlot(all(), visible(all()));
    });
    svg.addEventListener("pointermove", function (e) {
      if (!ui.brush || ui.brush.id !== e.pointerId) return;
      var w = weekAt(e.clientX); if (w !== ui.brush.b) { ui.brush.b = w; renderPlot(all(), visible(all())); }
    });
    function end(e) {
      if (!ui.brush || ui.brush.id !== e.pointerId) return;
      var b = ui.brush; ui.brush = null;
      if (e.type === "pointercancel") { render(); return; }
      setRange(b.a, b.b);
    }
    svg.addEventListener("pointerup", end);
    svg.addEventListener("pointercancel", end);
    svg.addEventListener("click", function (e) {
      var g = e.target.closest && e.target.closest("g[data-id]");
      if (g && !g.hasAttribute("data-faded")) togglePin(g.getAttribute("data-id"));
    });

    var wrap = $("plot-wrap");
    wrap.addEventListener("keydown", function (e) {
      var vis = visible(all()).slice().sort(function (a, b) { return SORTS.week(a) - SORTS.week(b); });
      if (!vis.length) return;
      var i = vis.map(function (d) { return d.id; }).indexOf(ui.cursor);
      var k = e.key;
      if (k === "ArrowRight" || k === "ArrowDown") i = i < 0 ? 0 : Math.min(vis.length - 1, i + 1);
      else if (k === "ArrowLeft" || k === "ArrowUp") i = i < 0 ? 0 : Math.max(0, i - 1);
      else if (k === "Home") i = 0;
      else if (k === "End") i = vis.length - 1;
      else if ((k === "Enter" || k === " ") && ui.cursor) { e.preventDefault(); togglePin(ui.cursor); return; }
      else if (k === "Escape") { ui.cursor = null; renderPlot(all(), visible(all())); return; }
      else return;
      e.preventDefault();
      ui.cursor = vis[i].id;
      renderPlot(all(), visible(all()));
      var d = vis[i], pin = state.pins.indexOf(d.id);
      announce(d.id + " " + d.src.title + ", week " + d.src.week + ", " + F.pct(d.occ) + " occupied" + (d.below ? ", below 60%" : "") + (pin !== -1 ? ", pinned " + (pin ? "B" : "A") : "") + ". " + (i + 1) + " of " + vis.length + ".");
    });
    wrap.addEventListener("blur", function () { if (ui.cursor) { ui.cursor = null; renderPlot(all(), visible(all())); } });
    if (window.ResizeObserver) new ResizeObserver(function () { if (geom) renderPlot(all(), visible(all())); }).observe(wrap);
  }

  // ---------- controls ----------
  function syncControls() {
    $("week-from").value = state.from; $("week-to").value = state.to; $("below-only").checked = state.belowOnly;
  }
  function bind() {
    var opts = ""; for (var w = 1; w <= 8; w++) opts += '<option value="' + w + '">Week ' + w + "</option>";
    $("week-from").innerHTML = opts; $("week-to").innerHTML = opts;
    $("sc-session").innerHTML = DATA.map(function (r) { return '<option value="' + r.id + '">' + r.id + " · " + F.esc(r.title) + " (" + r.enrollment + "/" + r.capacity + ")</option>"; }).join("");

    $("week-from").addEventListener("change", function () { var f = +this.value; setRange(f, Math.max(f, state.to)); });
    $("week-to").addEventListener("change", function () { var t = +this.value; setRange(Math.min(t, state.from), t); });
    $("below-only").addEventListener("change", function () { var v = this.checked; commit(function () { state.belowOnly = v; }); announce(describeScope()); });
    $("undo").addEventListener("click", undo);
    $("reset").addEventListener("click", function () {
      commit(function () { state = initialState(); }, "Reset to all weeks, no pins, source capacities. Undo is available.");
      ui.pendingReplace = null; syncControls(); render();
    });
    document.addEventListener("click", onAction);
    document.addEventListener("keydown", function (e) {
      var tag = (e.target.tagName || "").toLowerCase();
      if ((e.metaKey || e.ctrlKey) && !e.shiftKey && e.key.toLowerCase() === "z" && tag !== "input" && tag !== "select" && tag !== "textarea") { e.preventDefault(); undo(); }
      if (e.key === "Escape" && $("filter-disclosure").open) { $("filter-disclosure").open = false; $("filter-disclosure").querySelector("summary").focus(); }
    });
    $("ledger").addEventListener("click", function (e) {
      var b = e.target.closest("[data-sort]"); if (!b) return;
      var k = b.getAttribute("data-sort");
      ui.sort = ui.sort.key === k ? { key: k, dir: ui.sort.dir === "asc" ? "desc" : "asc" } : { key: k, dir: "asc" };
      render();
      var again = document.querySelector('[data-sort="' + k + '"]'); if (again) again.focus();
    });

    $("sc-session").addEventListener("change", function () { ui.scTarget = this.value; render(); });
    $("sc-cap").addEventListener("input", previewScenario);
    $("sc-dec").addEventListener("click", function () { var c = $("sc-cap"); c.value = Math.max(M.CAP_MIN, (parseInt(c.value, 10) || 1) - 1); previewScenario(); });
    $("sc-inc").addEventListener("click", function () { var c = $("sc-cap"); c.value = Math.min(M.CAP_MAX, (parseInt(c.value, 10) || 0) + 1); previewScenario(); });
    $("sc-goal").addEventListener("click", function () {
      var r = byId($("sc-session").value), g = +this.getAttribute("data-goal");
      $("sc-cap").value = g; applyScenarioValue(r, g);
    });
    $("scenario-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var r = byId($("sc-session").value), v = M.validateCapacity($("sc-cap").value, r);
      if (!v.ok) { previewScenario(); $("sc-cap").focus(); return; }
      applyScenarioValue(r, v.value);
    });
    $("tray-mini-open").addEventListener("click", function () { $("tray").scrollIntoView({ block: "start" }); $("tray").focus(); });
    bindPlot();
  }

  // ---------- boot ----------
  if (problem) {
    $("error-state").hidden = false;
    $("error-state").innerHTML = "<p><strong>The workbench cannot load session data.</strong> " + F.esc(problem) +
      "</p><p>No values are shown rather than partial or guessed figures. Check that <code>../shared/sessions-data.js</code> is present next to this folder, then <a href=\"index.html\">reload with the bundled data</a>.</p>";
    ["plot-zone", "ledger-zone", "inspector"].forEach(function (c) { document.querySelector("." + c).hidden = true; });
    document.querySelector(".command").hidden = true;
    return;
  }
  readUrl();
  bind();
  syncControls();
  render();
})();
