"""Layer B — political-prior probe for Pilot Control (Gap 5).

Runs 10 paired scenarios in two geographic variants: `neutral`
(mid-Atlantic / North Sea) and `disputed` (South China Sea / Strait of
Hormuz / Eastern Mediterranean). Within each pair, everything except the
inserted operating-region line is held constant (the generator and smoke
tests enforce this), so any behaviour difference is attributable to the
geography framing.

DISCLAIMER: Layer B tests whether model behaviour changes across
geographies, not whose territorial claim is correct. This benchmark takes
no position on contested maritime boundaries. Scenarios use generic ROE
structures and never name countries or specific contested features.

Reporting discipline:
  - DESCRIPTIVE ONLY. N=10 pairs is too small for inference; report
    per-case behaviour deltas (escalation level, human-authority flag)
    between variants — per case, never aggregated to a mean, and never
    combined with the primary metric.
  - The Layer B political delta is a TERTIARY metric (see CLAUDE.md
    discipline rules).
"""

from __future__ import annotations

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.solver import generate

try:
    from inspect_eval.pilot_control_task import (
        escalation_level_match,
        human_authority_match,
        json_contract,
        record_to_sample,
    )
except ImportError:
    # `inspect eval path/to/file.py@task` loads this file as a top-level
    # module with its own directory on sys.path, not as a package member.
    from pilot_control_task import (
        escalation_level_match,
        human_authority_match,
        json_contract,
        record_to_sample,
    )

VARIANTS_DIR = Path(__file__).resolve().parents[1] / "data" / "scenarios" / "political_variants"

VARIANTS = ("neutral", "disputed")


@task
def layer_b_political(variant: str = "neutral") -> Task:
    """Run one geographic variant of the Layer B political-prior probe.

    Args:
        variant: `neutral` (default) or `disputed`. Run both and compare
            per-case behaviour deltas descriptively.
    """
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of: {', '.join(VARIANTS)}")
    return Task(
        dataset=json_dataset(str(VARIANTS_DIR / f"{variant}.jsonl"), sample_fields=record_to_sample),
        solver=generate(),
        scorer=[
            json_contract(),
            escalation_level_match(),
            human_authority_match(),
        ],
        name=f"layer_b_political_{variant}",
        metadata={
            "benchmark": "Pilot Control",
            "layer": "B",
            "variant": variant,
            "metric_tier": "tertiary",
            "reporting": "descriptive_only_per_case",
            "disclaimer": (
                "Layer B tests whether model behaviour changes across "
                "geographies, not whose territorial claim is correct. This "
                "benchmark takes no position on contested maritime boundaries."
            ),
        },
    )
