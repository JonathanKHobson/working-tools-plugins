/*
 * Editorial alternative (martini-glass sequence, after Segel & Heer 2010):
 * author-led chapters (seats → pair → what-if) that open into reader-led exploration.
 * Every generated sentence is recomputed from the current scope and states that scope.
 * Depends on ../shared/sessions-data.js and ../shared/session-model.js (classic scripts).
 */
(function () {
  "use strict";
  var M = window.SessionModel, F = M.fmt;
  var $ = function (id) { return document.getElementById(id); };
  var params = new URLSearchParams(location.search);
  var DATA = params.get("state") === "error" ? null : window.SESSION_DATA;
  var problem = M.validate(DATA);

  var state = initial();
  function initial() { return { from: 1, to: 8, belowOnly: false, pair: [null, null], pairChosen: false, scenario: {}, wiTarget: null }; }
  function byId(id) { for (var i = 0; i < DATA.length; i++) if (DATA[i].id === id) return DATA[i]; return null; }
  function announce(m) { $("announcer").textContent = ""; setTimeout(function () { $("announcer").textContent = m; }, 30); }
  function rowsAll() { return M.derive(DATA, state.scenario); }
  function vis(rows) { return M.applyFilters(rows, state); }
  function scopeWords() { return state.from === 1 && state.to === 8 ? "Across all eight weeks" : (state.from === state.to ? "In week " + state.from : "In weeks " + state.from + "–" + state.to); }
  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }

  // ---------- URL ----------
  function readUrl() {
    var f = parseInt(params.get("from"), 10), t = parseInt(params.get("to"), 10);
    if (f >= 1 && f <= 8) state.from = f;
    if (t >= 1 && t <= 8) state.to = t;
    if (state.from > state.to) { var x = state.from; state.from = state.to; state.to = x; }
    state.belowOnly = params.get("below") === "1";
    var p1 = params.get("p1"), p2 = params.get("p2");
    if (p1 && byId(p1)) { state.pair[0] = p1; state.pairChosen = true; }
    if (p2 && byId(p2) && p2 !== p1) { state.pair[1] = p2; state.pairChosen = true; }
    (params.get("sc") || "").split(",").forEach(function (p) {
      var kv = p.split(":"), r = byId(kv[0]); if (!r) return;
      var v = M.validateCapacity(kv[1], r); if (v.ok && v.value !== r.capacity) state.scenario[r.id] = v.value;
    });
    var wi = params.get("wi"); if (wi && byId(wi)) state.wiTarget = wi;
  }
  function writeUrl() {
    var q = new URLSearchParams();
    if (state.from !== 1) q.set("from", state.from);
    if (state.to !== 8) q.set("to", state.to);
    if (state.belowOnly) q.set("below", "1");
    if (state.pairChosen) { if (state.pair[0]) q.set("p1", state.pair[0]); if (state.pair[1]) q.set("p2", state.pair[1]); }
    var sc = Object.keys(state.scenario).map(function (k) { return k + ":" + state.scenario[k]; });
    if (sc.length) q.set("sc", sc.join(","));
    if (state.wiTarget) q.set("wi", state.wiTarget);
    var s = q.toString();
    try { window.history.replaceState(null, "", (s ? "?" + s : location.pathname) + location.hash); } catch (e) { /* file:// restrictions */ }
  }

  // ---------- render ----------
  function render() {
    var rows = rowsAll(), v = vis(rows);
    renderStandfirst(v);
    renderRibbon(v);
    renderSeatmap(v, rows);
    renderNotes(v);
    renderPair(v, rows);
    renderWhatIf(rows);
    renderExplore(v, rows);
    writeUrl();
  }

  function renderStandfirst(v) {
    var el = $("standfirst");
    if (!v.length) { el.innerHTML = scopeWords() + ", no session matches the current filters. <a href=\"#explore\">Widen the scope in chapter 4.</a>"; return; }
    var p = M.pooled(v, false), below = v.filter(function (d) { return d.below; }).length;
    var s = scopeWords() + ", <strong>" + p.enrollment + " of " + p.capacity + " seats</strong> were filled (" + F.pct(p.occ) + "). ";
    if (state.belowOnly) s += "You are reading only the " + plural(v.length, "session", "sessions") + " that filled fewer than 60% of their seats.";
    else s += "<strong>" + below + " of " + v.length + "</strong> " + (v.length === 1 ? "session" : "sessions") + " filled fewer than 60% of their seats.";
    if (Object.keys(state.scenario).length) s += " These are recorded figures; chapter 3’s hypothetical capacity is not included.";
    el.innerHTML = s;
  }

  function renderRibbon(v) {
    var t = "Reading " + (state.from === 1 && state.to === 8 ? "all weeks" : "weeks " + state.from + "–" + state.to) + " · " + v.length + " of " + DATA.length + " sessions" + (state.belowOnly ? " · below 60% only" : "");
    var ids = Object.keys(state.scenario);
    $("ribbon-text").innerHTML = F.esc(t) + (ids.length ? '<span class="hyp-tag">Hypothetical: ' + ids.map(function (id) { return id + " " + byId(id).capacity + "→" + state.scenario[id] + " seats"; }).join(", ") + "</span>" : "");
  }

  function seatsHtml(enrollment, sourceCap, effCap) {
    var n = Math.max(sourceCap, effCap), h = "";
    for (var i = 0; i < n; i++) {
      var cls = i < enrollment ? "f" : (i < Math.min(sourceCap, effCap) ? "o" : (effCap < sourceCap ? "removed" : "added"));
      h += '<span class="seat ' + cls + '"></span>';
    }
    var notchAt = 0.6 * effCap;
    h += '<span class="notch" style="left: calc((var(--seat-size) + var(--seat-gap)) * ' + notchAt + ' - var(--seat-gap) / 2 - 1px)"></span>';
    return '<div class="seats" aria-hidden="true">' + h + "</div>";
  }

  function rowLabel(d) {
    return d.id + " " + d.src.title + ", week " + d.src.week + ": " + d.src.enrollment + " of " + d.src.capacity + " seats filled, " + F.pct(d.occ) +
      (d.below ? ", below 60 percent" : "") + (d.scenario ? ". Hypothetical capacity " + d.effCapacity + " would give " + F.pct(d.effOcc) : "") +
      ". " + (state.pair.indexOf(d.id) !== -1 ? "In the side-by-side reading." : "Select to add to the side-by-side reading.");
  }

  function renderSeatmap(v, rows) {
    var map = $("seatmap"), empty = $("seat-empty");
    if (!v.length) { map.innerHTML = ""; empty.hidden = false; empty.innerHTML = emptyHtml(rows); return; }
    empty.hidden = true;
    var h = "", lastWeek = null;
    v.forEach(function (d) {
      if (d.src.week !== lastWeek) { h += '<div class="week-rule">Week ' + d.src.week + "</div>"; lastWeek = d.src.week; }
      var inPair = state.pair.indexOf(d.id) !== -1;
      h += '<button type="button" class="seat-row" data-id="' + d.id + '" aria-pressed="' + inPair + '" aria-label="' + F.esc(rowLabel(d)) + '">' +
        '<span class="seat-name">' + F.esc(d.src.title) + '<span class="meta">' + d.id + " · " + d.src.enrollment + " of " + d.src.capacity + " filled · " +
        (d.below ? '<span class="below">' + F.pct(d.occ) + " — below 60%</span>" : F.pct(d.occ)) +
        (d.scenario ? ' · <span class="hyp">hypothetical ' + d.effCapacity + " seats → " + F.pct(d.effOcc) + "</span>" : "") + "</span></span>" +
        seatsHtml(d.src.enrollment, d.src.capacity, d.effCapacity) + "</button>";
    });
    map.innerHTML = h;
  }

  function renderNotes(v) {
    var el = $("margin-notes");
    if (!v.length) { el.innerHTML = ""; return; }
    var notes = [];
    var maxOpen = Math.max.apply(null, v.map(function (d) { return d.src.capacity - d.src.enrollment; }));
    var mo = v.filter(function (d) { return d.src.capacity - d.src.enrollment === maxOpen; });
    notes.push(["Most empty seats", mo.map(function (d) { return d.id + " " + d.src.title; }).join(" and ") + " — " + maxOpen + " open."]);
    var minOcc = Math.min.apply(null, v.map(function (d) { return d.occ; }));
    var lo = v.filter(function (d) { return d.occ === minOcc; });
    notes.push(["Lowest occupancy", lo.map(function (d) { return d.id + " — " + F.pct(d.occ) + " (" + d.src.enrollment + " of " + d.src.capacity + ")"; }).join("; ") + "."]);
    var at = v.filter(function (d) { return d.src.enrollment * 100 === M.THRESHOLD_PCT * d.src.capacity; });
    if (at.length) notes.push(["Exactly on the line", at.map(function (d) { return d.id; }).join(", ") + " filled exactly 60% and is not counted as below."]);
    var none = v.filter(function (d) { return d.noRatings; });
    if (none.length) notes.push(["Missing feedback", none.map(function (d) { return d.id; }).join(", ") + " has no ratings yet. Response counts for the other sessions appear with each mean; sampling and comparability are unknown."]);
    el.innerHTML = '<p class="visually-hidden">Notes computed for ' + scopeWords().toLowerCase() + ".</p>" + notes.map(function (n) { return '<p><span class="label">' + n[0] + "</span>" + F.esc(n[1]) + "</p>"; }).join("");
  }

  function defaultPair(v) {
    return v.slice().sort(function (a, b) {
      return (b.src.capacity - b.src.enrollment) - (a.src.capacity - a.src.enrollment) || a.occ - b.occ || (a.id < b.id ? -1 : 1);
    }).slice(0, 2).map(function (d) { return d.id; });
  }

  function renderPair(v, rows) {
    if (!state.pairChosen) { var dp = defaultPair(v); state.pair = [dp[0] || null, dp[1] || null]; }
    $("pick-1").value = state.pair[0] || ""; $("pick-2").value = state.pair[1] || "";
    $("pair-rule").innerHTML = state.pairChosen
      ? 'Your chosen pair. <button type="button" class="link-btn" data-action="default-pair">Return to the starting pair</button>'
      : "Starting pair: the two sessions in this scope with the most unfilled seats. Choose any two, here or by selecting rows in chapter 1.";
    var find = function (id) { return rows.filter(function (d) { return d.id === id; })[0]; };
    var A = state.pair[0] && find(state.pair[0]), B = state.pair[1] && find(state.pair[1]);
    if (!A || !B) { $("pair").innerHTML = '<p class="caveat">Choose two different sessions to read them side by side.</p>'; return; }
    var visIds = v.map(function (d) { return d.id; });
    var outside = [A, B].filter(function (d) { return visIds.indexOf(d.id) === -1; }).map(function (d) { return d.id; });
    var strips = [A, B].map(function (d) {
      return '<div class="pair-strip"><span class="who"><strong>' + d.id + "</strong> " + F.esc(d.src.title) + "</span>" + seatsHtml(d.src.enrollment, d.src.capacity, d.src.capacity) + "</div>";
    }).join("");
    var diff = (B.occ - A.occ) * 100;
    var occS = Math.abs(diff) < 0.05 ? "Their occupancy is the same." : (diff > 0 ? B.id : A.id) + " is " + Math.abs(diff).toFixed(1) + " points higher.";
    var sentence = A.id + " filled " + A.src.enrollment + " of its " + A.src.capacity + " seats (" + F.pct(A.occ) + "); " + B.id + " filled " + B.src.enrollment + " of " + B.src.capacity + " (" + F.pct(B.occ) + "). " + occS +
      " " + A.id + " leaves " + (A.src.capacity - A.src.enrollment) + " seats open; " + B.id + " leaves " + (B.src.capacity - B.src.enrollment) + ".";
    var c = M.compare(A, B);
    var ratingNote = c.ratingDifference === null
      ? "No rating difference is available because at least one session has no responses."
      : "The descriptive difference between recorded rating means is " + (c.ratingDifference >= 0 ? "+" : "−") + Math.abs(c.ratingDifference).toFixed(1) + " / 5 (B − A). Response counts are shown beside each mean. Sampling and comparability are unknown; this is not a significance test.";
    var tr = function (k, a, b) { return '<tr><th scope="row">' + k + "</th><td>" + a + "</td><td>" + b + "</td></tr>"; };
    var stanza = '<table class="stanza"><caption class="visually-hidden">Recorded values for ' + A.id + " and " + B.id + '</caption><thead><tr><th scope="col"></th><th scope="col">' + A.id + '</th><th scope="col">' + B.id + "</th></tr></thead><tbody>" +
      tr("Week.", A.src.week, B.src.week) +
      tr("Filled.", A.src.enrollment + " of " + A.src.capacity + " · " + F.pct(A.occ), B.src.enrollment + " of " + B.src.capacity + " · " + F.pct(B.occ)) +
      tr("Open.", A.src.capacity - A.src.enrollment + " seats", B.src.capacity - B.src.enrollment + " seats") +
      tr("Rated.", F.rating(A.src), F.rating(B.src)) +
      tr("Cost.", F.usd(A.src.cost_usd) + " · " + F.usd2(A.costPerEnrolled) + " per participant", F.usd(B.src.cost_usd) + " · " + F.usd2(B.costPerEnrolled) + " per participant") +
      "</tbody></table>";
    var cav = ratingNote;
    if (outside.length) cav += " " + outside.join(" and ") + (outside.length > 1 ? " are" : " is") + " outside the weeks you are reading and kept here by choice.";
    if (A.scenario || B.scenario) cav += " These are recorded capacities; chapter 3’s hypothetical values are not used here.";
    $("pair").innerHTML = '<div class="pair-strips" aria-hidden="true">' + strips + '</div><p class="pair-sentence">' + F.esc(sentence) + "</p>" + stanza + '<p class="caveat">' + F.esc(cav) + "</p>";
  }

  function renderWhatIf(rows) {
    if (!state.wiTarget) state.wiTarget = state.pair[0] || "S04";
    var r = byId(state.wiTarget), d = rows.filter(function (x) { return x.id === r.id; })[0];
    $("wi-session").value = r.id;
    var range = $("wi-cap");
    range.min = Math.max(M.CAP_MIN, r.enrollment);
    range.max = Math.max(r.capacity, Math.min(40, r.capacity + 8));
    range.value = d.effCapacity;
    $("wi-out").textContent = d.effCapacity;
    range.setAttribute("aria-valuetext", d.effCapacity + " seats, " + F.pct(d.effOcc) + " full" + (d.scenario ? ", hypothetical" : ", as recorded"));
    $("wi-strip").innerHTML = seatsHtml(r.enrollment, r.capacity, d.effCapacity);
    var s;
    if (!d.scenario) {
      s = r.id + " " + F.esc(r.title) + ": " + r.enrollment + " of " + r.capacity + " seats filled (" + F.pct(d.occ) + "), as recorded. Move the slider to try a different room size.";
    } else {
      s = '<span class="hyp-word">Hypothetically</span>, with ' + d.effCapacity + " seats instead of " + r.capacity + ", " + r.id + " would be " + F.pct(d.effOcc) + " full — " +
        (d.effBelow ? "still below" : "at or above") + " the 60% line. Enrollment is held at " + r.enrollment + ". This is not a forecast.";
    }
    $("wi-sentence").innerHTML = s;
    var goal = M.capacityForThreshold(r.enrollment), gb = $("wi-goal");
    if (!d.below || goal == null) { gb.disabled = true; gb.textContent = "Already at or above 60% as recorded"; }
    else { gb.disabled = false; gb.textContent = "Try " + goal + " seats — the largest room still at least 60% full"; gb.setAttribute("data-goal", goal); }
    var rb = $("wi-restore");
    rb.textContent = "Restore recorded capacity (" + r.capacity + ")"; rb.disabled = !d.scenario;
    var ids = Object.keys(state.scenario);
    $("wi-active").innerHTML = ids.length ? '<ul class="active-list" aria-label="Hypothetical changes in effect">' + ids.map(function (id) {
      return "<li><span>" + id + ": " + byId(id).capacity + " → " + state.scenario[id] + ' seats (hypothetical)</span><button type="button" class="btn quiet" data-action="restore" data-id="' + id + '">Restore ' + id + "</button></li>";
    }).join("") + '</ul><div class="row-actions" style="margin-top:8px"><button type="button" class="btn quiet" data-action="restore-all">Restore all recorded capacities</button></div>' : "";
  }

  function emptyHtml(rows) {
    var why = M.explainEmpty(rows, state);
    if (why.cause === "below") {
      return "<p><strong>No session in weeks " + state.from + "–" + state.to + " is below 60% occupied.</strong> Those weeks hold " + plural(why.inWeekRange, "session", "sessions") + ", all at or above the line.</p>" +
        '<div class="row-actions"><button type="button" class="btn" data-action="clear-below">Show all occupancy levels</button><button type="button" class="btn quiet" data-action="all-weeks">Keep the filter, read all weeks (' + why.belowAnywhere + ")</button></div>";
    }
    return "<p><strong>No sessions are scheduled in weeks " + state.from + "–" + state.to + ".</strong></p>" +
      '<div class="row-actions"><button type="button" class="btn" data-action="all-weeks">Read all weeks</button></div>';
  }

  function renderExplore(v, rows) {
    document.querySelectorAll("[data-preset]").forEach(function (b) {
      var p = b.getAttribute("data-preset").split("-");
      b.setAttribute("aria-pressed", String(+p[0] === state.from && +p[1] === state.to));
    });
    $("ex-from").value = state.from; $("ex-to").value = state.to; $("ex-below").checked = state.belowOnly;
    var e = $("ex-empty");
    if (!v.length) { e.hidden = false; e.innerHTML = emptyHtml(rows); } else { e.hidden = true; e.innerHTML = ""; }
    var head = "<caption>" + plural(v.length, "session", "sessions") + " · " + scopeWords() + " · calendar order · recorded values, hypothetical in its own column</caption>" +
      '<thead><tr><th scope="col">ID</th><th scope="col">Session</th><th scope="col">Week</th><th scope="col">Enrolled</th><th scope="col">Capacity</th><th scope="col">Occupancy</th><th scope="col">Rating</th><th scope="col">Responses</th><th scope="col">Cost</th><th scope="col">Per participant</th><th scope="col">Hypothetical</th></tr></thead>';
    var body = v.map(function (d) {
      return "<tr><td>" + d.id + "</td><td>" + F.esc(d.src.title) + "</td><td>" + d.src.week + "</td><td>" + d.src.enrollment + "</td><td>" + d.src.capacity + "</td><td>" +
        (d.below ? '<span class="below">' + F.pct(d.occ) + " below 60%</span>" : F.pct(d.occ)) + "</td><td>" + (d.noRatings ? "none yet" : d.src.rating.toFixed(1)) + "</td><td>" + d.src.response_count +
        "</td><td>" + F.usd(d.src.cost_usd) + "</td><td>" + F.usd2(d.costPerEnrolled) + "</td><td>" + (d.scenario ? '<span class="hyp">' + d.effCapacity + " seats → " + F.pct(d.effOcc) + "</span>" : "") + "</td></tr>";
    }).join("");
    $("ex-table").innerHTML = head + "<tbody>" + (body || '<tr><td colspan="11">No sessions in this scope.</td></tr>') + "</tbody>";
  }

  // ---------- actions ----------
  function setScope(from, to, below, focusEl) {
    state.from = Math.min(from, to); state.to = Math.max(from, to);
    if (below !== undefined) state.belowOnly = below;
    render();
    announce($("ribbon-text").textContent + ". Sentences above now describe this scope.");
    if (focusEl) focusEl.focus();
  }

  function togglePairFromRow(id) {
    var idx = state.pair.indexOf(id), r = byId(id);
    state.pairChosen = true;
    if (idx !== -1) { state.pair[idx] = null; announce(r.title + " removed from the side-by-side reading."); }
    else if (!state.pair[0]) { state.pair[0] = id; announce(r.title + " is the first session in chapter 2."); }
    else if (!state.pair[1]) { state.pair[1] = id; announce(r.title + " is the second session in chapter 2."); }
    else { var old = byId(state.pair[1]); state.pair[1] = id; announce(r.title + " replaced " + old.title + " as the second session in chapter 2."); }
    render();
    var again = document.querySelector('.seat-row[data-id="' + id + '"]'); if (again) again.focus();
  }

  function bind() {
    var opts = ""; for (var w = 1; w <= 8; w++) opts += '<option value="' + w + '">Week ' + w + "</option>";
    $("ex-from").innerHTML = opts; $("ex-to").innerHTML = opts;
    var sopts = DATA.map(function (r) { return '<option value="' + r.id + '">' + r.id + " · " + F.esc(r.title) + " (week " + r.week + ")</option>"; }).join("");
    $("pick-1").innerHTML = '<option value="">— choose —</option>' + sopts;
    $("pick-2").innerHTML = '<option value="">— choose —</option>' + sopts;
    $("wi-session").innerHTML = sopts;

    $("seatmap").addEventListener("click", function (e) { var b = e.target.closest(".seat-row"); if (b) togglePairFromRow(b.getAttribute("data-id")); });

    [["pick-1", 0], ["pick-2", 1]].forEach(function (p) {
      $(p[0]).addEventListener("change", function () {
        var other = state.pair[1 - p[1]], val = this.value || null;
        if (val && val === other) { $("pair-error").textContent = "Choose two different sessions."; this.value = state.pair[p[1]] || ""; return; }
        $("pair-error").textContent = "";
        if (!state.pairChosen) { state.pair = state.pair.slice(); state.pairChosen = true; }
        state.pair[p[1]] = val; render();
      });
    });

    $("wi-session").addEventListener("change", function () { state.wiTarget = this.value; render(); });
    $("wi-cap").addEventListener("input", function () {
      var r = byId(state.wiTarget), v = M.validateCapacity(this.value, r);
      if (!v.ok) return; // range min/max already prevent this; kept as a guard
      if (v.value === r.capacity) delete state.scenario[r.id]; else state.scenario[r.id] = v.value;
      render();
    });
    $("wi-cap").addEventListener("change", function () {
      var r = byId(state.wiTarget), d = rowsAll().filter(function (x) { return x.id === r.id; })[0];
      announce(d.scenario ? "Hypothetical: " + d.effCapacity + " seats, " + F.pct(d.effOcc) + " full. Source unchanged." : "Recorded capacity " + r.capacity + " seats.");
    });
    $("wi-goal").addEventListener("click", function () {
      var r = byId(state.wiTarget), g = +this.getAttribute("data-goal");
      state.scenario[r.id] = g; render();
      announce("Hypothetical: " + g + " seats gives " + F.pct(r.enrollment / g) + " for " + r.id + ". Source unchanged.");
      $("wi-cap").focus();
    });
    $("wi-restore").addEventListener("click", function () {
      var r = byId(state.wiTarget); delete state.scenario[r.id]; render();
      announce("Restored recorded capacity for " + r.id + ": " + r.capacity + " seats."); $("wi-cap").focus();
    });

    document.querySelectorAll("[data-preset]").forEach(function (b) {
      b.addEventListener("click", function () { var p = this.getAttribute("data-preset").split("-"); setScope(+p[0], +p[1]); });
    });
    $("ex-from").addEventListener("change", function () { var f = +this.value; setScope(f, Math.max(f, state.to)); });
    $("ex-to").addEventListener("change", function () { var t = +this.value; setScope(Math.min(t, state.from), t); });
    $("ex-below").addEventListener("change", function () { setScope(state.from, state.to, this.checked); });

    $("ribbon-reset").addEventListener("click", function () {
      state = initial(); render();
      announce("Reset: all weeks, all occupancy levels, starting pair, recorded capacities.");
    });

    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-action]"); if (!t) return;
      var a = t.getAttribute("data-action"), id = t.getAttribute("data-id");
      if (a === "clear-below") setScope(state.from, state.to, false, $("h-explore"));
      else if (a === "all-weeks") setScope(1, 8, undefined, $("h-explore"));
      else if (a === "default-pair") { state.pairChosen = false; render(); announce("Starting pair restored."); $("h-pair").focus(); }
      else if (a === "restore") { delete state.scenario[id]; render(); announce("Restored recorded capacity for " + id + "."); $("h-whatif").focus(); }
      else if (a === "restore-all") { state.scenario = {}; render(); announce("All recorded capacities restored."); $("h-whatif").focus(); }
    });
  }

  // ---------- boot ----------
  if (problem) {
    $("error-state").hidden = false;
    $("error-state").innerHTML = "<p><strong>This page cannot load its session data.</strong> " + F.esc(problem) +
      "</p><p>No figures are shown rather than partial or guessed ones. Check that <code>../shared/sessions-data.js</code> is present, then <a href=\"index.html\">reload with the bundled data</a>.</p>";
    document.querySelectorAll(".chapter, .ribbon, .chapters").forEach(function (n) { n.hidden = true; });
    $("standfirst").textContent = "Data unavailable.";
    return;
  }
  readUrl();
  bind();
  render();
})();
