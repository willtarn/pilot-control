"""Smoke tests. Run in CI on every PR; fast (<5s)."""

import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_package_imports():
    """The Inspect task module imports cleanly."""
    from inspect_eval import pilot_control_task  # noqa: F401
    from inspect_eval import tools  # noqa: F401


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
