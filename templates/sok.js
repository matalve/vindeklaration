// Search runs entirely in the browser against one gzipped index. No requests
// leave this site once the page has loaded, and there is nothing to log.
//
// Column order matches build_index() in src/site.py. Change one, change both.
var COL = {
  NR: 0, NAME: 1, PRODUCER: 2, VINTAGE: 3, PRICE: 4, STATE: 5, COUNT: 6,
  COUNTRY: 7, CATEGORY: 8, ASSORTMENT: 9, GRAPES: 10, PAIRINGS: 11,
  ADDITIVES: 12, STOCK: 13, URL: 14
};

function normalise(text) {
  return text.toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g, "");
}

// A result row says the declaration state in words and never shows a bottle
// photograph: legal-notes §2j condition 8 keeps images off every ranked or
// filtered surface, and a row of them would also read as a shelf.
function stateLabel(row) {
  if (row[COL.STATE] === "d") {
    return row[COL.COUNT] === 0
      ? window.SITE.stateDeclaredZero
      : window.SITE.stateDeclared + " " + row[COL.COUNT];
  }
  if (row[COL.STATE] === "p") return window.SITE.statePartial;
  return window.SITE.stateSilent;
}

function loadIndex(onReady, onProgress) {
  if (window.SITE._data) {
    onReady(window.SITE._data);
    return;
  }
  if (window.SITE._loading) return;
  window.SITE._loading = true;
  if (onProgress) onProgress();
  fetch(window.SITE.index)
    .then(function (r) { return r.json(); })
    .then(function (payload) {
      payload.wines.forEach(function (row) {
        row._n = normalise(row[COL.NAME]);
        row._p = normalise(row[COL.PRODUCER]);
      });
      window.SITE._data = payload;
      window.SITE._loading = false;
      onReady(payload);
    });
}

(function () {
  var input = document.getElementById("q");
  if (!input) return;
  var list = document.getElementById("results");
  var hint = document.getElementById("hint");

  function render(rows, total) {
    list.innerHTML = "";
    if (!rows.length) {
      hint.textContent = window.SITE.noResults;
      return;
    }
    hint.textContent =
      rows.length < total
        ? window.SITE.showing + " " + rows.length + " " + window.SITE.of +
          " " + total + " " + window.SITE.resultsCount
        : total + " " + window.SITE.resultsCount;
    var frag = document.createDocumentFragment();
    rows.forEach(function (row) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "/" + row[COL.URL] + "/";
      a.textContent = row[COL.NAME] + (row[COL.VINTAGE] ? " " + row[COL.VINTAGE] : "");
      var meta = document.createElement("span");
      meta.className = "meta";
      meta.textContent = [
        row[COL.PRODUCER],
        window.SITE._data.vocab.country[row[COL.COUNTRY]],
        row[COL.PRICE] ? Math.round(row[COL.PRICE]) + " kr" : ""
      ].filter(Boolean).join(" · ");
      var state = document.createElement("span");
      state.className = "state state-" + row[COL.STATE];
      state.textContent = stateLabel(row);
      li.appendChild(a);
      li.appendChild(meta);
      li.appendChild(state);
      frag.appendChild(li);
    });
    list.appendChild(frag);
  }

  function search(query) {
    var data = window.SITE._data;
    if (!data) return;
    var q = normalise(query.trim());
    if (q.length < 2) {
      list.innerHTML = "";
      hint.textContent = window.SITE.hint;
      return;
    }
    // A bare number is almost always an article number off a shelf label.
    var byNumber = /^\d+$/.test(q);
    var hits = [];
    for (var i = 0; i < data.wines.length; i++) {
      var row = data.wines[i];
      var match = byNumber
        ? row[COL.NR].indexOf(q) === 0
        : row._n.indexOf(q) !== -1 || row._p.indexOf(q) !== -1;
      if (match) hits.push(row);
    }
    render(hits.slice(0, 50), hits.length);
  }

  function go() {
    loadIndex(function () { search(input.value); },
              function () { hint.textContent = "…"; });
  }

  // The index is a couple of megabytes uncompressed, so it is fetched on the
  // first keystroke rather than on load — the front page has to be readable on
  // a shop's signal.
  input.addEventListener("focus", go, { once: true });
  input.addEventListener("input", go);
})();
