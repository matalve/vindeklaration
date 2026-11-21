"""The Worker reads the dataset bucket and never writes it.

Preview builds bind the production bucket (the `previews` block in
wrangler.jsonc, which `wrangler preview` insists on). That is safe only while
the Worker never writes: a preview of a branch that did would be writing to
production. These tests are what keeps the choice honest.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def config() -> dict:
    """wrangler.jsonc without its full-line comments."""
    lines = (ROOT / "wrangler.jsonc").read_text(encoding="utf-8").splitlines()
    return json.loads("\n".join(l for l in lines if not l.lstrip().startswith("//")))


def test_the_worker_only_reads_the_bucket() -> None:
    code = (ROOT / "worker" / "index.js").read_text(encoding="utf-8")
    code = re.sub(r"//.*", "", code)
    assert set(re.findall(r"env\.DATA\.(\w+)", code)) == {"get"}


def test_only_get_and_head_reach_the_bucket() -> None:
    code = (ROOT / "worker" / "index.js").read_text(encoding="utf-8")
    guard = re.search(
        r'request\.method !== "GET" && request\.method !== "HEAD"\)\s*\{\s*'
        r'return new Response\("Method not allowed", \{ status: 405 \}\)',
        code,
    )
    assert guard
    assert code.index(guard.group(0)) < code.index("env.DATA.get")


def test_every_bucket_the_worker_binds_is_also_bound_for_previews() -> None:
    """Without it `wrangler preview` stops with "missing a `previews` block"."""
    cfg = config()
    bound = {b["binding"] for b in cfg["r2_buckets"]}
    previewed = {b["binding"] for b in cfg.get("previews", {}).get("r2_buckets", [])}
    assert bound <= previewed
