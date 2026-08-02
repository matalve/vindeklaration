// The filter's menu pruning, run against the real index.
//
// `available()` decides which options the reader is offered, so an error in it
// hides wines that exist rather than merely looking wrong. It is checked here
// against a brute-force re-slice: for a sample of values, filter the whole
// index the slow obvious way and assert the fast one-pass answer agrees.
//
//   node --test tests/test_hitta.mjs
//
// Needs a built index. `uv run python -m src.site --output site` makes one.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import vm from "node:vm";

const INDEX = ["site/sok-index.json", "/tmp/sitefull/sok-index.json"]
  .find(existsSync);
if (!INDEX) {
  throw new Error("no built index found — run: uv run python -m src.site --output site");
}

const data = JSON.parse(readFileSync(INDEX, "utf8"));

// A stale index is worse than none: every row still parses, every menu still
// renders, and the threshold tests quietly pass against a column that is not
// there. `site/` is gitignored and survives across branches, so this happens.
const COLUMNS = 16;
if (data.wines[0].length !== COLUMNS) {
  throw new Error(
    `${INDEX} has ${data.wines[0].length} columns, expected ${COLUMNS} — ` +
    "it predates a change to build_index(). Rebuild it.",
  );
}

// Load the two browser files into one context. They expect a DOM; the pieces
// under test do not touch it, so a stub that yields no form is enough to keep
// the IIFE from running while still defining COL and the helpers.
const context = vm.createContext({
  window: { SITE: {} },
  document: { getElementById: () => null },
});
for (const file of ["templates/sok.js", "templates/hitta.js"]) {
  vm.runInContext(readFileSync(file, "utf8"), context);
}
// `available` lives inside the IIFE, so it is re-evaluated here from the same
// source rather than exported — the alternative is a module system this site
// deliberately does not have.
const source = readFileSync("templates/hitta.js", "utf8");
const body = source.slice(source.indexOf("var FACETS ="), source.indexOf("function prune("));
const available = vm.runInContext(
  `(function (COL, FIXED_RANGE) { ${body}; return available; })`,
  context,
)(context.COL, "Fast sortiment");

const COL = context.COL;
const none = {
  today: false, category: null, assortment: null, country: null,
  grape: null, pairing: null, maxPrice: null, minStores: null,
};

// The slow, obviously-correct version: keep every wine matching all criteria,
// then read off which values survive.
function bruteForce(criteria, facet) {
  const values = new Set();
  for (const w of data.wines) {
    if (w[COL.STOCK] !== 0) continue;
    if (criteria.today && data.vocab.assortment[w[COL.ASSORTMENT]] !== "Fast sortiment") continue;
    if (criteria.category !== null && w[COL.CATEGORY] !== criteria.category) continue;
    if (criteria.assortment !== null && w[COL.ASSORTMENT] !== criteria.assortment) continue;
    if (criteria.country !== null && w[COL.COUNTRY] !== criteria.country) continue;
    if (criteria.grape !== null && w[COL.GRAPES].indexOf(criteria.grape) === -1) continue;
    if (criteria.pairing !== null && w[COL.PAIRINGS].indexOf(criteria.pairing) === -1) continue;
    if (criteria.minStores !== null
      && (w[COL.STORES] === null || w[COL.STORES] < criteria.minStores)) continue;
    if (criteria.maxPrice && (w[COL.PRICE] === null || w[COL.PRICE] > criteria.maxPrice)) continue;
    if (facet === "grape") w[COL.GRAPES].forEach((g) => values.add(g));
    else if (facet === "pairing") w[COL.PAIRINGS].forEach((p) => values.add(p));
    else if (facet === "country") values.add(w[COL.COUNTRY]);
    else if (facet === "category") values.add(w[COL.CATEGORY]);
  }
  return values;
}

test("an offered grape always holds at least one wine", () => {
  // France, where the long tail of grapes is longest.
  const france = data.vocab.country.indexOf("Frankrike");
  assert.notEqual(france, -1);
  const c = { ...none, country: france };
  const offered = Object.keys(available(data, c).grape).map(Number);

  assert.ok(offered.length > 0);
  const real = bruteForce(c, "grape");
  for (const g of offered) {
    assert.ok(real.has(g), `grape ${data.vocab.grape[g]} offered but holds nothing`);
  }
});

test("no grape that holds a wine is hidden", () => {
  const france = data.vocab.country.indexOf("Frankrike");
  const c = { ...none, country: france };
  const offered = new Set(Object.keys(available(data, c).grape).map(Number));
  for (const g of bruteForce(c, "grape")) {
    assert.ok(offered.has(g), `grape ${data.vocab.grape[g]} hidden but holds a wine`);
  }
});

test("the pruning is symmetric: countries narrow to a chosen grape", () => {
  // Sangiovese is essentially Italian, so the country menu should collapse.
  const grape = data.vocab.grape.indexOf("Sangiovese");
  assert.notEqual(grape, -1);
  const c = { ...none, grape };
  const offered = new Set(Object.keys(available(data, c).country).map(Number));

  assert.deepEqual(offered, bruteForce(c, "country"));
  assert.ok(offered.size < data.vocab.country.length,
    "choosing Sangiovese should hide at least one country");
});

test("two active criteria still leave every remaining menu correct", () => {
  const country = data.vocab.country.indexOf("Italien");
  const category = data.vocab.category.indexOf("Rött vin");
  const c = { ...none, country, category, maxPrice: 150 };

  assert.deepEqual(
    new Set(Object.keys(available(data, c).grape).map(Number)),
    bruteForce(c, "grape"),
  );
  assert.deepEqual(
    new Set(Object.keys(available(data, c).pairing).map(Number)),
    bruteForce(c, "pairing"),
  );
});

test("a facet's own value never restricts its own menu", () => {
  // Choosing one country must not reduce the country menu to that country —
  // otherwise the reader could never switch to another without clearing first.
  const italy = data.vocab.country.indexOf("Italien");
  const offered = Object.keys(available(data, { ...none, country: italy }).country);

  assert.ok(offered.length > 1,
    "the country menu collapsed to the chosen country and became a dead end");
});

test("the store threshold narrows the other menus", () => {
  const wide = available(data, { ...none, minStores: 150 });
  const all = available(data, none);

  assert.ok(Object.keys(wide.grape).length < Object.keys(all.grape).length,
    "requiring 150 stores should hide grapes that only appear in the long tail");
  assert.deepEqual(
    new Set(Object.keys(wide.grape).map(Number)),
    bruteForce({ ...none, minStores: 150 }, "grape"),
  );
});

// `prune` is the half the reader actually touches. Extracted the same way, and
// driven against stub <option>s rather than a real DOM.
const pruneSource = source.slice(source.indexOf("function prune("), source.indexOf("function pruneMenus("));
function makePrune(select) {
  const ctx = vm.createContext({ document: { getElementById: () => select } });
  return vm.runInContext(`${pruneSource}; prune`, ctx);
}
const options = (...values) => values.map((v) => ({ value: v, hidden: false, disabled: false }));

test("the empty option is never pruned away", () => {
  const select = { value: "", options: options("", "3", "9") };
  makePrune(select)("f-country", () => false);

  assert.equal(select.options[0].hidden, false, "clearing the filter became impossible");
});

test("the current selection is never hidden, even when it holds nothing", () => {
  // Reachable only by changing another control first — say the reader picks a
  // grape, then narrows the country until that grape holds nothing. Hiding the
  // value they are looking at would change the answer without saying so.
  const select = { value: "7", options: options("", "7", "8") };
  const buried = makePrune(select)("f-grape", () => false);

  assert.equal(select.options[1].hidden, false);
  assert.equal(select.options[1].disabled, false);
  assert.equal(buried, 1, "only the unselected empty value should be counted");
});

test("an option holding nothing is both hidden and disabled", () => {
  // `hidden` on an <option> is honoured unevenly across browsers, so the
  // fallback has to make it unselectable rather than merely invisible.
  const select = { value: "", options: options("", "4") };
  makePrune(select)("f-grape", () => false);

  assert.equal(select.options[1].hidden, true);
  assert.equal(select.options[1].disabled, true);
});

test("pruning is reversible: an option comes back when it holds again", () => {
  const select = { value: "", options: options("", "4") };
  const prune = makePrune(select);
  prune("f-grape", () => false);
  prune("f-grape", () => true);

  assert.equal(select.options[1].hidden, false, "clearing a filter must restore the menu");
  assert.equal(select.options[1].disabled, false);
});

test("one pass over the index stays quick enough to run on every keystroke", () => {
  const c = { ...none, country: data.vocab.country.indexOf("Italien") };
  const started = process.hrtime.bigint();
  for (let i = 0; i < 5; i++) available(data, c);
  const perCall = Number(process.hrtime.bigint() - started) / 5 / 1e6;

  assert.ok(perCall < 120, `${perCall.toFixed(0)} ms per call is too slow to type against`);
});
