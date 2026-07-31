// The shortlist builder. Filters and ranks in the browser against the same
// index the search uses; nothing is sent anywhere.
//
// The rules it implements are in docs/site-plan.md and are not incidental:
//
// * A slice is shown in three blocks, never collapsed into one list. Only the
//   first is ranked, because it is the only one where a count exists.
// * Undeclared wines stay in the results. Someone shopping for a Riesling is
//   shopping for a Riesling, and hiding four bottles in five because their
//   supplier wrote nothing is a shorter answer, not a better one.
// * An additive filter labels the undeclared block, it never removes it. There
//   is nothing there to match against, and absence of a declaration is not
//   evidence of an empty bottle.
// * Every count that is shown says what it counts and why wines are missing.

(function () {
  var form = document.getElementById("filters");
  if (!form) return;

  var out = document.getElementById("slice");
  var status = document.getElementById("slice-status");
  var S = window.SITE;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  }

  // Systembolaget publishes these in Swedish. On the English build they are
  // looked up; a value with no entry stays Swedish, which is meant to be
  // visible rather than silently plausible.
  function label(kind, value) {
    var table = S.facetLabels && S.facetLabels[kind];
    return (table && table[value]) || value;
  }

  function fillSelect(id, kind, values, keep) {
    var sel = document.getElementById(id);
    if (!sel) return;
    var order = values.map(function (v, i) { return [kind ? label(kind, v) : v, i]; })
                      .filter(function (p) { return p[0]; })
                      .sort(function (a, b) { return a[0].localeCompare(b[0], S.lang); });
    order.forEach(function (p) {
      var o = document.createElement("option");
      o.value = p[1];
      o.textContent = p[0];
      sel.appendChild(o);
    });
    if (keep !== undefined) sel.value = keep;
  }

  function chosen(id) {
    var sel = document.getElementById(id);
    return sel && sel.value !== "" ? parseInt(sel.value, 10) : null;
  }

  function criteria() {
    return {
      buyable: document.getElementById("f-buyable").checked,
      category: chosen("f-category"),
      country: chosen("f-country"),
      grape: chosen("f-grape"),
      pairing: chosen("f-pairing"),
      maxPrice: (function (v) {
        return v === "" || isNaN(parseFloat(v)) ? null : parseFloat(v);
      })(document.getElementById("f-price").value),
      exclude: chosen("f-exclude"),
      include: chosen("f-include")
    };
  }

  // The facets split into two kinds and the difference has to reach the reader.
  // Price, country, category and buyability are complete: a wine either matches
  // or does not. Grape and food pairing are filled for roughly 57% and 27% of
  // the catalogue, so selecting one silently discards every wine whose field is
  // empty — a gap in Systembolaget's metadata, not a supplier's silence. Those
  // two are counted separately so the results page can say which is which.
  function slice(data, c) {
    var kept = [], dropped = { grape: 0, pairing: 0, stock: 0 };
    for (var i = 0; i < data.wines.length; i++) {
      var w = data.wines[i];
      if (c.buyable && w[COL.STOCK] !== 0) { dropped.stock++; continue; }
      if (c.category !== null && w[COL.CATEGORY] !== c.category) continue;
      if (c.country !== null && w[COL.COUNTRY] !== c.country) continue;
      if (c.maxPrice && (w[COL.PRICE] === null || w[COL.PRICE] > c.maxPrice)) continue;
      // Counted apart, because the causes differ: an empty grape field is
      // Systembolaget's missing metadata, an empty pairing field likewise, and
      // summing them into one number tells the reader neither.
      if (c.grape !== null && w[COL.GRAPES].length === 0) { dropped.grape++; continue; }
      if (c.pairing !== null && w[COL.PAIRINGS].length === 0) { dropped.pairing++; continue; }
      if (c.grape !== null && w[COL.GRAPES].indexOf(c.grape) === -1) continue;
      if (c.pairing !== null && w[COL.PAIRINGS].indexOf(c.pairing) === -1) continue;
      kept.push(w);
    }
    return { kept: kept, dropped: dropped };
  }

  // Applies to block 1 and to nothing else. Exclude is sound only where the
  // declaration was read in full: a wine that declared everything and did not
  // list the substance genuinely does not contain it. Blocks 2 and 3 are, by
  // definition, the wines whose declaration was not read in full or does not
  // exist — they can neither confirm nor deny a choice, so filtering them would
  // answer a question they never got to answer. They are labelled instead.
  function bySubstance(rows, c) {
    if (c.exclude === null && c.include === null) return rows;
    return rows.filter(function (w) {
      if (c.exclude !== null && w[COL.ADDITIVES].indexOf(c.exclude) !== -1) return false;
      if (c.include !== null && w[COL.ADDITIVES].indexOf(c.include) === -1) return false;
      return true;
    });
  }

  function row(w) {
    var li = el("li");
    var a = el("a");
    a.href = "/" + w[COL.URL] + "/";
    a.textContent = w[COL.NAME] + (w[COL.VINTAGE] ? " " + w[COL.VINTAGE] : "");
    li.appendChild(a);
    li.appendChild(el("span", "meta", [
      w[COL.PRODUCER],
      label("country", window.SITE._data.vocab.country[w[COL.COUNTRY]]),
      w[COL.PRICE] ? Math.round(w[COL.PRICE]) + " kr" : "",
      label("assortment", window.SITE._data.vocab.assortment[w[COL.ASSORTMENT]])
    ].filter(Boolean).join(" · ")));
    li.appendChild(el("span", "state state-" + w[COL.STATE], stateLabel(w)));
    return li;
  }

  function block(title, note, rows, limit) {
    var sec = el("section", "block");
    sec.appendChild(el("h3", null, title + " (" + rows.length + ")"));
    if (note) sec.appendChild(el("p", "explain", note));
    var ol = el("ol", "results");
    rows.slice(0, limit).forEach(function (w) { ol.appendChild(row(w)); });
    sec.appendChild(ol);
    if (rows.length > limit) {
      sec.appendChild(el("p", "explain",
        S.showing + " " + limit + " " + S.of + " " + rows.length + "."));
    }
    return sec;
  }

  function render(data) {
    var c = criteria();
    var s = slice(data, c);
    var declared = [], partial = [], silent = [];
    s.kept.forEach(function (w) {
      if (w[COL.STATE] === "d") declared.push(w);
      else if (w[COL.STATE] === "p") partial.push(w);
      else silent.push(w);
    });

    var rankable = bySubstance(declared, c);
    var bySubstanceDropped = declared.length - rankable.length;
    var substanceChosen = c.exclude !== null || c.include !== null;

    rankable.sort(function (a, b) {
      if (a[COL.COUNT] !== b[COL.COUNT]) return a[COL.COUNT] - b[COL.COUNT];
      return (a[COL.PRICE] || 0) - (b[COL.PRICE] || 0);
    });

    // Every wine that left the catalogue on the way to this page gets a line of
    // its own. Summing them, or omitting one, leaves the reader with a total
    // that does not reconcile against anything else on the site.
    var lines = [S.sliceHeld.replace("{n}", s.kept.length)];
    if (s.dropped.stock) lines.push(S.stockDropped.replace("{n}", s.dropped.stock));
    if (s.dropped.grape) lines.push(S.grapeDropped.replace("{n}", s.dropped.grape));
    if (s.dropped.pairing) lines.push(S.pairingDropped.replace("{n}", s.dropped.pairing));
    if (bySubstanceDropped) {
      lines.push(S.substanceDropped.replace("{n}", bySubstanceDropped));
    }
    status.textContent = lines.join(" ");

    out.innerHTML = "";
    if (!s.kept.length) {
      out.appendChild(el("p", "explain", S.noResults));
      return;
    }

    // No ranking without a comparison set. A sparkling wine declares dosage
    // sugar and a fortified wine declares added alcohol, so ordering them
    // against a still red asserts a comparability that does not exist — the
    // plan forbids a global "fewest additives" table by name, and rendering one
    // by default is the same table with nobody having asked for it.
    if (c.category === null) {
      var ask = el("section", "block need-category");
      ask.appendChild(el("h3", null,
        S.needCategory + " (" + rankable.length + ")"));
      ask.appendChild(el("p", "explain", S.needCategoryWhy));
      out.appendChild(ask);
    } else {
      out.appendChild(block(S.blockRanked, S.blockRankedNote, rankable, 50));
    }

    // Always rendered, including at zero. Three states means three headings —
    // a block that vanishes when a filter empties it is indistinguishable from
    // a slice that never held one, and the plan forbids the silent drop.
    out.appendChild(block(
      S.blockPartial,
      substanceChosen ? S.blockPartialFiltered : S.blockPartialNote,
      partial, 20));

    // Never filtered by substance, only labelled. This block is the reason the
    // site exists and removing it would answer a question nobody asked.
    out.appendChild(block(
      S.blockSilent,
      substanceChosen ? S.blockSilentFiltered : S.blockSilentNote,
      silent, 20));
  }

  function start() {
    loadIndex(function (data) {
      fillSelect("f-category", "category", data.vocab.category);
      fillSelect("f-country", "country", data.vocab.country);
      // Grape names are the same in both languages; Systembolaget already
      // normalises them and there is nothing to translate.
      fillSelect("f-grape", null, data.vocab.grape);
      fillSelect("f-pairing", "pairing", data.vocab.pairing);
      var substances = data.vocab.additive.map(function (id) {
        return S.additiveNames[id] || id;
      });
      fillSelect("f-exclude", null, substances);
      fillSelect("f-include", null, substances);
      form.hidden = false;
      form.addEventListener("input", function () { render(data); });
      render(data);
    }, function () { status.textContent = "…"; });
  }

  start();
})();
