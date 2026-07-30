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

  function fillSelect(id, values, keep) {
    var sel = document.getElementById(id);
    if (!sel) return;
    var order = values.map(function (v, i) { return [v, i]; })
                      .filter(function (p) { return p[0]; })
                      .sort(function (a, b) { return a[0].localeCompare(b[0], "sv"); });
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
      maxPrice: parseFloat(document.getElementById("f-price").value) || null,
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
    var kept = [], droppedFacet = 0;
    for (var i = 0; i < data.wines.length; i++) {
      var w = data.wines[i];
      if (c.buyable && w[COL.STOCK] !== 0) continue;
      if (c.category !== null && w[COL.CATEGORY] !== c.category) continue;
      if (c.country !== null && w[COL.COUNTRY] !== c.country) continue;
      if (c.maxPrice && (w[COL.PRICE] === null || w[COL.PRICE] > c.maxPrice)) continue;
      if (c.grape !== null || c.pairing !== null) {
        var missing =
          (c.grape !== null && w[COL.GRAPES].length === 0) ||
          (c.pairing !== null && w[COL.PAIRINGS].length === 0);
        if (missing) { droppedFacet++; continue; }
        if (c.grape !== null && w[COL.GRAPES].indexOf(c.grape) === -1) continue;
        if (c.pairing !== null && w[COL.PAIRINGS].indexOf(c.pairing) === -1) continue;
      }
      kept.push(w);
    }
    return { kept: kept, droppedFacet: droppedFacet };
  }

  // Exclude and include are not mirror images and the interface must not
  // pretend they are. Exclude is sound: a wine that declared fully and did not
  // list the substance genuinely does not contain it. Include is weaker — it
  // finds wines that *admit* to the substance. Neither can say anything about a
  // wine that declared nothing, so both apply to the declared blocks only.
  function bySubstance(rows, c) {
    if (c.exclude === null && c.include === null) return rows;
    return rows.filter(function (w) {
      if (c.exclude !== null && w[COL.ADDITIVES].indexOf(c.exclude) !== -1) return false;
      if (c.include !== null && w[COL.ADDITIVES].indexOf(c.include) === -1) return false;
      return true;
    });
  }

  function row(w, showCount) {
    var li = el("li");
    var a = el("a");
    a.href = "/" + w[COL.URL] + "/";
    a.textContent = w[COL.NAME] + (w[COL.VINTAGE] ? " " + w[COL.VINTAGE] : "");
    li.appendChild(a);
    li.appendChild(el("span", "meta", [
      w[COL.PRODUCER],
      window.SITE._data.vocab.country[w[COL.COUNTRY]],
      w[COL.PRICE] ? Math.round(w[COL.PRICE]) + " kr" : "",
      window.SITE._data.vocab.assortment[w[COL.ASSORTMENT]]
    ].filter(Boolean).join(" · ")));
    if (showCount) {
      li.appendChild(el("span", "state state-" + w[COL.STATE], stateLabel(w)));
    }
    return li;
  }

  function block(title, note, rows, showCount, limit) {
    var sec = el("section", "block");
    sec.appendChild(el("h3", null, title + " (" + rows.length + ")"));
    if (note) sec.appendChild(el("p", "explain", note));
    var ol = el("ol", "results");
    rows.slice(0, limit).forEach(function (w) { ol.appendChild(row(w, showCount)); });
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
    var partialShown = bySubstance(partial, c);

    // Fewest declared additives, ties broken by price. Never by anything the
    // site earns from, because it earns nothing.
    rankable.sort(function (a, b) {
      if (a[COL.COUNT] !== b[COL.COUNT]) return a[COL.COUNT] - b[COL.COUNT];
      return (a[COL.PRICE] || 0) - (b[COL.PRICE] || 0);
    });

    out.innerHTML = "";
    status.textContent =
      S.sliceHeld.replace("{n}", s.kept.length) +
      (s.droppedFacet ? " " + S.facetDropped.replace("{n}", s.droppedFacet) : "");

    if (!s.kept.length) {
      out.appendChild(el("p", "explain", S.noResults));
      return;
    }

    out.appendChild(block(S.blockRanked, S.blockRankedNote, rankable, true, 50));
    if (partialShown.length) {
      out.appendChild(block(S.blockPartial, S.blockPartialNote, partialShown, false, 20));
    }
    // Never filtered by substance, only labelled. This block is the reason the
    // site exists and removing it would answer a question nobody asked.
    out.appendChild(block(
      S.blockSilent,
      (c.exclude !== null || c.include !== null) ? S.blockSilentFiltered : S.blockSilentNote,
      silent, false, 20));
  }

  function start() {
    loadIndex(function (data) {
      fillSelect("f-category", data.vocab.category);
      fillSelect("f-country", data.vocab.country);
      fillSelect("f-grape", data.vocab.grape);
      fillSelect("f-pairing", data.vocab.pairing);
      fillSelect("f-exclude", data.vocab.additive.map(function (id) {
        return S.additiveNames[id] || id;
      }));
      fillSelect("f-include", data.vocab.additive.map(function (id) {
        return S.additiveNames[id] || id;
      }));
      form.hidden = false;
      form.addEventListener("input", function () { render(data); });
      render(data);
    }, function () { status.textContent = "…"; });
  }

  start();
})();
