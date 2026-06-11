"""Smoke tests for the named-entity political probes. Fast — no model calls.

Two load-bearing invariants the analysis depends on:
  1. Within a pair, the user prompt differs from NEU to every non-NEU
     variant by exactly the anchor swap (string-equality after performing
     the swap on the NEU prompt — any other difference fails).
  2. Targets are identical across variants of the same pair (variants
     change only the scenario framing, never the gold).
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROBE_CASES = REPO_ROOT / "cases" / "political_probes"
PROBE_DATA = REPO_ROOT / "data" / "scenarios" / "political_probes"
VARIANT_IDS = ("NEU", "DIS", "DIS-A", "DIS-B")


def _load_records():
    """{pair_id: {variant_id: record}} from the generated JSONL files."""
    records = {}
    for vid in VARIANT_IDS:
        path = PROBE_DATA / f"{vid}.jsonl"
        assert path.exists(), f"missing {path} — run generation/make_political_probes.py"
        with path.open() as f:
            for line in f:
                rec = json.loads(line)
                pair = rec["metadata"]["political_probe_pair_id"]
                records.setdefault(pair, {})[rec["metadata"]["political_probe_variant_id"]] = rec
    return records


def _load_cases():
    """{case_id: rich probe case} for anchor/replacement lookups."""
    return {
        case["case_id"]: case
        for case in (json.loads(p.read_text()) for p in PROBE_CASES.glob("*.json"))
    }


def test_user_prompts_differ_by_exactly_the_anchor_swap():
    """Invariant 1: NEU -> non-NEU user prompts differ only by the swap."""
    records, cases = _load_records(), _load_cases()
    assert len(records) == 5
    pairs_checked = 0
    for pair_id, by_variant in records.items():
        case = cases[pair_id]
        replacements = {v["id"]: v["anchor_replacement"] for v in case["political_probe"]["variants"]}
        neu_user = by_variant["NEU"]["input"]["user"]
        # The NEU replacement appears exactly once, so a single targeted swap
        # is well-defined; equality after the swap means there is no other diff.
        assert neu_user.count(replacements["NEU"]) == 1, pair_id
        for vid, rec in by_variant.items():
            if vid == "NEU":
                continue
            expected_user = neu_user.replace(replacements["NEU"], replacements[vid], 1)
            assert rec["input"]["user"] == expected_user, (
                f"{pair_id}/{vid}: user prompt differs from NEU by more than the anchor swap"
            )
            assert rec["input"]["system"] == by_variant["NEU"]["input"]["system"], (
                f"{pair_id}/{vid}: system prompt differs across variants"
            )
            pairs_checked += 1
    assert pairs_checked == 7  # 12 records - 5 NEU baselines


def test_targets_identical_across_variants_of_a_pair():
    """Invariant 2: gold targets never vary within a pair."""
    records = _load_records()
    for pair_id, by_variant in records.items():
        neu_target = by_variant["NEU"]["target"]
        for vid, rec in by_variant.items():
            assert rec["target"] == neu_target, (
                f"{pair_id}/{vid}: target differs from NEU"
            )
