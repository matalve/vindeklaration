// Search runs entirely in the browser against one gzipped index. No requests
// leave this site once the page has loaded, and there is nothing to log.
(function () {
  var input = document.getElementById("q");
  var list = document.getElementById("results");
  var hint = document.getElementById("hint");
  var data = null;
  var loading = false;

  // A result row shows the declaration state in words. It never shows a bottle
  // photograph: docs/legal-notes.md §2j condition 8 keeps images off every
  // ranked or filtered page, and a row of images would also read as a shelf.
  function stateLabel(row) {
    if (row.s === "d") {
      return row.a === 0
        ? window.SITE.stateDeclaredZero
        : window.SITE.stateDeclared + " " + row.a;
    }
    if (row.s === "p") return window.SITE.statePartial;
    return window.SITE.stateSilent;
  }

  function normalise(text) {
    return text
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[̀-ͯ]/g, "");
  }

  function render(rows, total) {
    list.innerHTML = "";
    if (!rows.length) {
      hint.textContent = window.SITE.noResults;
      return;
    }
    hint.textContent = total + " " + window.SITE.resultsCount;
    var frag = document.createDocumentFragment();
    rows.forEach(function (row) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = window.SITE.base + "/" + row.u + "/";
      a.textContent = row.t + (row.v ? " " + row.v : "");
      var meta = document.createElement("span");
      meta.className = "meta";
      meta.textContent =
        [row.p, row.c, row.pr ? Math.round(row.pr) + " kr" : ""]
          .filter(Boolean)
          .join(" · ");
      var state = document.createElement("span");
      state.className = "state state-" + row.s;
      state.textContent = stateLabel(row);
      li.appendChild(a);
      li.appendChild(meta);
      li.appendChild(state);
      frag.appendChild(li);
    });
    list.appendChild(frag);
  }

  function search(query) {
    var q = normalise(query.trim());
    if (q.length < 2) {
      list.innerHTML = "";
      hint.textContent = window.SITE.hint;
      return;
    }
    // A bare number is almost always an article number off a shelf label.
    var byNumber = /^\d+$/.test(q);
    var hits = [];
    for (var i = 0; i < data.length; i++) {
      var row = data[i];
      var match = byNumber
        ? row.n.indexOf(q) === 0
        : row._t.indexOf(q) !== -1 || row._p.indexOf(q) !== -1;
      if (match) hits.push(row);
      if (hits.length > 400) break;
    }
    render(hits.slice(0, 50), hits.length);
  }

  function load() {
    if (data || loading) return;
    loading = true;
    hint.textContent = "…";
    fetch(window.SITE.index)
      .then(function (r) {
        return r.json();
      })
      .then(function (rows) {
        rows.forEach(function (row) {
          row._t = normalise(row.t);
          row._p = normalise(row.p);
        });
        data = rows;
        loading = false;
        search(input.value);
      });
  }

  // The index is a megabyte, so it is fetched on the first keystroke rather
  // than on load — the front page has to be readable on a shop's signal.
  input.addEventListener("focus", load, { once: true });
  input.addEventListener("input", function () {
    if (!data) {
      load();
      return;
    }
    search(input.value);
  });
})();
