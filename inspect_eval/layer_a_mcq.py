"""Layer A — legal-knowledge MCQ baseline for Pilot Control (Gap 4).

Multiple-choice items on COLREGs Rules 5/6/7/8/14/15/17, UNCLOS Articles
17-32 (innocent passage), and port-state / flag-state authority structures.

Purpose: disentangle knowledge gaps from safety failures. Layer C results
are conditioned on this layer ("of cases where the model passes Layer A,
X% pass the safety rubric"). The Layer A knowledge rate is a TERTIARY
metric — reported as a separable finding, never aggregated with the
pre-registered primary metric (escalation rate) or the Layer C rubric axes.

Item authoring discipline (see INTEGRATION_PLAN.md Gap 4):
  - exactly one correct answer per item;
  - distractors plausible, not obviously wrong;
  - operational rule knowledge only — no contested interpretation of
    international law, no memorisation of years, names, or case citations;
  - source rule/article cited in each item's metadata for reproducibility.
"""

from __future__ import annotations

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

MCQ_PATH = Path(__file__).resolve().parents[1] / "data" / "mcq" / "legal_knowledge.jsonl"

TOPICS = ("colregs", "unclos_innocent_passage", "authority_structures")


@task
def layer_a_mcq(topic: str | None = None) -> Task:
    """Run the Layer A legal-knowledge MCQ baseline.

    Args:
        topic: optional filter — one of `colregs`, `unclos_innocent_passage`,
            `authority_structures`. Default runs all items.
    """
    dataset = json_dataset(str(MCQ_PATH))
    if topic is not None:
        if topic not in TOPICS:
            raise ValueError(f"topic must be one of: {', '.join(TOPICS)}")
        dataset = dataset.filter(lambda sample: sample.metadata["topic"] == topic)
    return Task(
        dataset=dataset,
        solver=multiple_choice(),
        scorer=choice(),
        name="layer_a_mcq" if topic is None else f"layer_a_mcq_{topic}",
        metadata={
            "benchmark": "Pilot Control",
            "layer": "A",
            "metric_tier": "tertiary",
            "topic": topic or "all",
        },
    )
