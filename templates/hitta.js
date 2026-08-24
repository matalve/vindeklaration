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

// Systembolaget's own name for the shelf range. Matched by value rather than
// by index because the index order comes from whatever the crawl saw first.
var FIXED_RANGE = "Fast sortiment";

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
      // "Today" means the fixed range and in stock — what is on a shelf. The
      // other mode drops only the range constraint, since an order-only wine is
      // still a wine you can have, just not this afternoon.
      today: document.getElementById("m-today").checked,
      category: chosen("f-category"),
      assortment: chosen("f-assortment"),
      country: chosen("f-country"),
      grape: chosen("f-grape"),
      pairing: chosen("f-pairing"),
      maxPrice: (function (v) {
        return v === "" || isNaN(parseFloat(v)) ? null : parseFloat(v);
      })(document.getElementById("f-price").value),
      exclude: chosen("f-exclude"),
      include: chosen("f-include"),
      minStores: chosen("f-stores")
    };
  }

  // The facets split into two kinds and the difference has to reach the reader.
  // Price, country, category and buyability are complete: a wine either matches
  // or does not. Grape and food pairing are filled for roughly 57% and 27% of
  // the catalogue, so selecting one silently discards every wine whose field is
  // empty — a gap in Systembolaget's metadata, not a supplier's silence. Those
  // two are counted separately so the results page can say which is which.
  function slice(data, c) {
    var kept = [], dropped = { grape: 0, pairing: 0, stock: 0, assortment: 0, stores: 0 };
    for (var i = 0; i < data.wines.length; i++) {
      var w = data.wines[i];
      if (w[COL.STOCK] !== 0) { dropped.stock++; continue; }
      if (c.today && data.vocab.assortment[w[COL.ASSORTMENT]] !== FIXED_RANGE) {
        dropped.assortment++; continue;
      }
      if (c.category !== null && w[COL.CATEGORY] !== c.category) continue;
      // Stock and range are different questions and were one control until
      // 2026-07-31. Four wines in five are order-only, of which almost none are
      // out of stock, so a single "can be ordered" checkbox answered the stock
      // question while its label implied the other.
      if (c.assortment !== null && w[COL.ASSORTMENT] !== c.assortment) {
        dropped.assortment++; continue;
      }
      if (c.country !== null && w[COL.COUNTRY] !== c.country) continue;
      if (c.maxPrice && (w[COL.PRICE] === null || w[COL.PRICE] > c.maxPrice)) continue;
      // Counted apart, because the causes differ: an empty grape field is
      // Systembolaget's missing metadata, an empty pairing field likewise, and
      // summing them into one number tells the reader neither.
      if (c.grape !== null && w[COL.GRAPES].length === 0) { dropped.grape++; continue; }
      if (c.pairing !== null && w[COL.PAIRINGS].length === 0) { dropped.pairing++; continue; }
      // Same shape as grape and pairing: a null is our own unread field, not
      // a wine that sits on no shelf, so it is counted apart rather than
      // silently failing the threshold.
      // `== null` on purpose: it catches undefined as well as null. A browser
      // holding a cached index from before this column existed would otherwise
      // read the missing value as passing every threshold, which is the one
      // failure mode that silently widens a result rather than narrowing it.
      if (c.minStores !== null) {
        if (w[COL.STORES] == null) { dropped.stores++; continue; }
        if (w[COL.STORES] < c.minStores) continue;
      }
      if (c.grape !== null && w[COL.GRAPES].indexOf(c.grape) === -1) continue;
      if (c.pairing !== null && w[COL.PAIRINGS].indexOf(c.pairing) === -1) continue;
      kept.push(w);
    }
    return { kept: kept, dropped: dropped };
  }

  // Which values are still worth offering. With 433 grapes against 57
  // countries most combinations hold nothing, and a menu that offers them is a
  // menu that answers "no wines match" to a question the reader could not have
  // known was empty.
  //
  // One pass, counting misses rather than re-slicing once per facet: a wine
  // that fails nothing is evidence for every menu, a wine that fails exactly
  // one criterion is evidence for that criterion's menu alone, and a wine that
  // fails two is evidence for none. Eight re-slices of 15 000 rows on every
  // keystroke is the obvious implementation and is the one that stutters on a
  // phone.
  var FACETS = ["category", "assortment", "country", "grape", "pairing", "stores"];

  function available(data, c) {
    var avail = {};
    FACETS.forEach(function (f) { avail[f] = {}; });

    for (var i = 0; i < data.wines.length; i++) {
      var w = data.wines[i];
      // Hard gates. Out of stock, or outside the range the mode asked for, and
      // the wine is not evidence for anything — it cannot be reached by any
      // menu choice without changing the mode first.
      if (w[COL.STOCK] !== 0) continue;
      if (c.today && data.vocab.assortment[w[COL.ASSORTMENT]] !== FIXED_RANGE) continue;

      // Inlined rather than pushed through a helper: this runs once per wine
      // per keystroke, and allocating a closure 15 000 times is the difference
      // the reader feels.
      var missed = null, misses = 0;
      if (c.category !== null && w[COL.CATEGORY] !== c.category) { missed = "category"; misses++; }
      if (c.assortment !== null && w[COL.ASSORTMENT] !== c.assortment) { missed = "assortment"; misses++; }
      if (c.country !== null && w[COL.COUNTRY] !== c.country) { missed = "country"; misses++; }
      if (misses > 1) continue;
      if (c.grape !== null && w[COL.GRAPES].indexOf(c.grape) === -1) { missed = "grape"; misses++; }
      if (c.pairing !== null && w[COL.PAIRINGS].indexOf(c.pairing) === -1) { missed = "pairing"; misses++; }
      if (misses > 1) continue;
      if (c.minStores !== null
        && (w[COL.STORES] == null || w[COL.STORES] < c.minStores)) { missed = "stores"; misses++; }
      // Price has no menu to prune, but it still has to be able to be the one
      // thing a wine failed, or a grape sold only above the cap would look
      // available.
      if (c.maxPrice && (w[COL.PRICE] === null || w[COL.PRICE] > c.maxPrice)) { missed = "price"; misses++; }
      if (misses > 1) continue;

      // A wine that failed one criterion is evidence only for that criterion's
      // own menu; one that failed nothing is evidence for all of them.
      FACETS.forEach(function (f) {
        if (misses === 1 && missed !== f) return;
        if (f === "grape") {
          w[COL.GRAPES].forEach(function (g) { avail.grape[g] = 1; });
        } else if (f === "pairing") {
          w[COL.PAIRINGS].forEach(function (p) { avail.pairing[p] = 1; });
        } else if (f === "stores") {
          if (w[COL.STORES] != null) avail.stores[w[COL.STORES]] = 1;
        } else if (f === "category") {
          avail.category[w[COL.CATEGORY]] = 1;
        } else if (f === "assortment") {
          avail.assortment[w[COL.ASSORTMENT]] = 1;
        } else {
          avail.country[w[COL.COUNTRY]] = 1;
        }
      });
    }
    return avail;
  }

  // Every option each menu could ever offer, captured once the menus are
  // filled, because pruning rebuilds them and would otherwise have nothing to
  // restore from.
  var MENUS = {};

  function snapshot(id) {
    var sel = document.getElementById(id);
    if (!sel) return;
    MENUS[id] = Array.prototype.map.call(sel.options, function (o) {
      return { value: o.value, text: o.textContent };
    });
  }

  // Rebuild the menu rather than toggle `hidden` on its options. Setting
  // `hidden` was the first implementation and it does not do the job: several
  // browsers render a hidden <option> anyway, and every native picker on a
  // phone renders a disabled one, so a 433-entry grape list stayed 433 entries
  // long and merely turned grey. Removing the nodes shortens the list
  // everywhere.
  //
  // Two things it must not do: drop the reader's own selection, which would
  // change the answer without saying so, and drop the empty option, which is
  // how a filter is cleared.
  function prune(id, ok) {
    var sel = document.getElementById(id);
    var all = MENUS[id];
    if (!sel || !all) return 0;

    var chosenValue = sel.value, keep = [], buried = 0;
    all.forEach(function (o) {
      if (o.value === "" || o.value === chosenValue || ok(o.value)) keep.push(o);
      else buried++;
    });

    // Never rebuild the control being used: replacing the options of an open
    // dropdown closes it under the reader's finger. It is pruned on the next
    // render, once they have moved on. The count is still reported, so the
    // status line does not flicker with the focus.
    if (document.activeElement !== sel && keep.length !== sel.options.length) {
      var frag = document.createDocumentFragment();
      keep.forEach(function (o) {
        var n = document.createElement("option");
        n.value = o.value;
        n.textContent = o.text;
        frag.appendChild(n);
      });
      sel.innerHTML = "";
      sel.appendChild(frag);
      sel.value = chosenValue;
    }
    return buried;
  }

  function pruneMenus(data, c, declaredAdditives) {
    var avail = available(data, c);
    var buried = 0;
    buried += prune("f-category", function (v) { return avail.category[v]; });
    buried += prune("f-assortment", function (v) { return avail.assortment[v]; });
    buried += prune("f-country", function (v) { return avail.country[v]; });
    buried += prune("f-grape", function (v) { return avail.grape[v]; });
    buried += prune("f-pairing", function (v) { return avail.pairing[v]; });
    // The thresholds are numbers, not ids: a threshold survives if any reachable
    // wine meets it.
    buried += prune("f-stores", function (v) {
      var need = parseInt(v, 10);
      for (var n in avail.stores) { if (parseInt(n, 10) >= need) return true; }
      return false;
    });
    // "Must declare" is the one substance menu worth pruning. Requiring a
    // substance nobody in the slice declares empties the ranked block, which is
    // a real dead end. Excluding one nobody declares is a no-op and removes
    // nothing, so that menu keeps every option.
    buried += prune("f-include", function (v) { return declaredAdditives[v]; });
    return buried;
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

    // What the declared wines in this slice actually name, so "must declare"
    // can drop the substances none of them do.
    var declaredAdditives = {};
    declared.forEach(function (w) {
      w[COL.ADDITIVES].forEach(function (a) { declaredAdditives[a] = 1; });
    });
    var buried = pruneMenus(data, c, declaredAdditives);

    rankable.sort(function (a, b) {
      if (a[COL.COUNT] !== b[COL.COUNT]) return a[COL.COUNT] - b[COL.COUNT];
      return (a[COL.PRICE] || 0) - (b[COL.PRICE] || 0);
    });

    // Every wine that left the catalogue on the way to this page gets a line of
    // its own. Summing them, or omitting one, leaves the reader with a total
    // that does not reconcile against anything else on the site.
    var lines = [S.sliceHeld.replace("{n}", s.kept.length)];
    if (s.dropped.stock) lines.push(S.stockDropped.replace("{n}", s.dropped.stock));
    if (s.dropped.assortment) {
      lines.push(S.assortmentDropped.replace("{n}", s.dropped.assortment));
    }
    if (s.dropped.grape) lines.push(S.grapeDropped.replace("{n}", s.dropped.grape));
    if (s.dropped.pairing) lines.push(S.pairingDropped.replace("{n}", s.dropped.pairing));
    if (s.dropped.stores) lines.push(S.storesDropped.replace("{n}", s.dropped.stores));
    if (bySubstanceDropped) {
      lines.push(S.substanceDropped.replace("{n}", bySubstanceDropped));
    }
    // The menus being shorter than they were is itself a fact about the data,
    // and an unexplained one reads as a bug or as the site deciding for you.
    if (buried) lines.push(S.optionsHidden.replace("{n}", buried));
    status.textContent = lines.join(" ");

    // The same figure in the chrome, where it stays visible while the reader
    // scrolls the results. A count and nothing else — the lines above are what
    // explain it, and they stay where they are.
    var badge = document.getElementById("header-count");
    if (badge) {
      badge.innerHTML = "";
      var n = document.createElement("b");
      n.textContent = s.kept.length.toLocaleString(S.lang === "sv" ? "sv-SE" : "en-GB");
      badge.appendChild(n);
      badge.appendChild(document.createTextNode(" " + S.winesWord));
    }

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
      fillSelect("f-assortment", "assortment", data.vocab.assortment);
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
      // After filling, before the first prune: this is the only moment the
      // menus are known to be complete.
      ["f-category", "f-assortment", "f-country", "f-grape", "f-pairing",
       "f-stores", "f-include"].forEach(snapshot);
      form.hidden = false;
      form.addEventListener("input", function () { render(data); });
      render(data);
    }, function () { status.textContent = "…"; });
  }

  start();
})();
