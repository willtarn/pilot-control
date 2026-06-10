"""Smoke tests. Run in CI on every PR; fast (<5s)."""

import csv
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_package_imports():
    """The Inspect task module imports cleanly."""
    from inspect_eval import (
        pilot_control_task,  # noqa: F401
        tools,  # noqa: F401
    )


def test_inspect_samples_are_valid_jsonl():
    """Inspect-ready records load and have the required top-level fields."""
    for split in ("all", "dev", "test"):
        path = REPO_ROOT / "data" / f"inspect_samples_{split}.jsonl"
        assert path.exists(), f"missing {path}"
        with path.open() as f:
            samples = [json.loads(line) for line in f if line.strip()]
        assert len(samples) > 0
        for s in samples:
            assert "id" in s
            assert "input" in s and "system" in s["input"] and "user" in s["input"]
            assert "target" in s
            assert "metadata" in s
            assert "scenario_family" in s["metadata"]


def test_split_counts():
    """Dev and test are 20 cases each; all is 40."""
    counts = {}
    for split in ("all", "dev", "test"):
        path = REPO_ROOT / "data" / f"inspect_samples_{split}.jsonl"
        with path.open() as f:
            counts[split] = sum(1 for line in f if line.strip())
    assert counts["all"] == 40
    assert counts["dev"] == 20
    assert counts["test"] == 20


def test_family_balance():
    """Each family has 5 cases in dev and 5 in test."""
    for split in ("dev", "test"):
        path = REPO_ROOT / "data" / f"inspect_samples_{split}.jsonl"
        families = {}
        with path.open() as f:
            for line in f:
                if not line.strip():
                    continue
                s = json.loads(line)
                fam = s["metadata"]["scenario_family"]
                families[fam] = families.get(fam, 0) + 1
        assert len(families) == 4, f"{split} has {len(families)} families, expected 4"
        for fam, n in families.items():
            assert n == 5, f"{split} family {fam} has {n} cases, expected 5"


def test_individual_case_files_match_summary():
    """Per-case JSONs in cases/ match the summary CSV count."""
    cases_dir = REPO_ROOT / "cases"
    summary_path = REPO_ROOT / "pilot_control_cases_summary.csv"
    case_files = list(cases_dir.glob("*.json"))
    assert len(case_files) == 40
    with summary_path.open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 40


def test_tools_module_exposes_four_tools():
    """The agent-condition tools module exposes the four expected tools."""
    from inspect_eval import tools

    for name in ("consult_roe", "check_weather", "request_human_authority", "log_decision"):
        assert hasattr(tools, name), f"missing tool: {name}"


def test_task_constructs_in_all_conditions():
    """Gap 1: the task builds without exceptions in each condition."""
    from inspect_eval.pilot_control_task import pilot_control

    for condition in ("direct", "cot", "agent"):
        task = pilot_control(split="dev", condition=condition)
        assert task is not None, f"task construction failed for condition {condition!r}"


def test_default_condition_is_direct():
    """Omitting `condition` preserves the original direct-only behaviour."""
    from inspect_eval.pilot_control_task import pilot_control

    task = pilot_control(split="dev")
    assert task.name == "pilot_control_dev"
    assert task.metadata["condition"] == "direct"


def test_invalid_condition_raises():
    """Unknown conditions are rejected up front, not at eval time."""
    from inspect_eval.pilot_control_task import pilot_control

    with pytest.raises(ValueError, match="condition"):
        pilot_control(split="dev", condition="bogus")


def test_graded_scorer_constructs():
    """Gap 3: the 5-axis graded scorer builds with default and custom graders."""
    from inspect_eval.scorers_graded import five_axis_graded

    assert five_axis_graded() is not None
    assert five_axis_graded(grader_model="openai/gpt-4o") is not None


def test_task_keeps_deterministic_scorers_and_adds_graded():
    """The graded scorer is additive: 5 deterministic scorers + 1 graded."""
    from inspect_eval.pilot_control_task import pilot_control

    task = pilot_control(split="dev")
    assert len(task.scorer) == 6


def test_same_model_guard_ignores_provider_prefix():
    """Subject/grader comparison strips provider and router prefixes."""
    from inspect_eval.scorers_graded import _model_key

    assert _model_key("openai/gpt-4o-mini") == _model_key("openrouter/openai/gpt-4o-mini")
    assert _model_key("anthropic/claude-sonnet-4") != _model_key("openai/gpt-4o-mini")


def test_layer_a_mcq_items_load_and_are_well_formed():
    """Gap 4: MCQ items parse, have 4 choices, a valid target, and source metadata."""
    path = REPO_ROOT / "data" / "mcq" / "legal_knowledge.jsonl"
    assert path.exists()
    items = [json.loads(line) for line in path.open() if line.strip()]
    assert 30 <= len(items) <= 50, f"expected 30-50 items, found {len(items)}"
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), "duplicate item ids"
    topics = set()
    for item in items:
        assert len(item["choices"]) == 4, f"{item['id']}: expected 4 choices"
        assert item["target"] in "ABCD", f"{item['id']}: bad target {item['target']!r}"
        assert item["metadata"].get("rule"), f"{item['id']}: missing source rule citation"
        topics.add(item["metadata"]["topic"])
    assert topics == {"colregs", "unclos_innocent_passage", "authority_structures"}


def test_layer_a_mcq_task_constructs():
    """The Layer A task builds, with and without a topic filter."""
    from inspect_eval.layer_a_mcq import layer_a_mcq

    assert layer_a_mcq() is not None
    assert layer_a_mcq(topic="colregs") is not None
    with pytest.raises(ValueError, match="topic"):
        layer_a_mcq(topic="bogus")


def test_all_cases_have_complete_rubric_annotations():
    """Every case carries all five axes with the credit tiers the grader consumes."""
    axes = {"correctness", "calibration", "escalation", "authority_respect", "colregs_roe_rule_following"}
    tiers = {"full_credit", "partial_credit", "no_credit", "key_observables"}
    path = REPO_ROOT / "data" / "inspect_samples_all.jsonl"
    with path.open() as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            rubric = record["metadata"]["rubric_annotations"]
            assert set(rubric) == axes, f"{record['id']}: axes {set(rubric)}"
            for axis, entry in rubric.items():
                assert tiers.issubset(entry), f"{record['id']}/{axis}: missing tiers"
