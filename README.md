# Pilot Control Maritime Safety Benchmark Dataset

This directory contains the structured scenario dataset for **Pilot Control: A Maritime Safety Benchmark for LLM Agents**. The release contains forty admitted behavioural-evaluation cases across four scenario families: maintenance deferral, anomaly triage, incident escalation, and autonomous-surface-vessel exception handling.

The dataset is designed for LLM-component evaluation, not for operational deployment. All ROE references are generic synthetic policy constraints used to test authority respect and escalation behaviour. They are not real-world military rules of engagement.

## Files

| File or directory | Description |
|---|---|
| `pilot_control_cases_all.json` | Full forty-case dataset as a JSON array. |
| `pilot_control_cases_dev.json` | Twenty-case development split. |
| `pilot_control_cases_test.json` | Twenty-case held-out test split. |
| `pilot_control_cases_all.jsonl` | Full dataset in JSON Lines format for Inspect-style ingestion. |
| `pilot_control_cases_summary.csv` | Compact tabular summary of case IDs, splits, gold decisions, escalation levels, and applicability tags. |
| `cases/` | Individual JSON files for all forty cases. |
| `dev/` and `test/` | Per-case JSON files partitioned by split. |
| `schema.md` | Dataset schema and controlled vocabularies. |
| `research_notes.md` | Reference notes for COLREGs, UNCLOS, and MASS/autonomy assumptions. |
| `validation_report.md` | Schema and split validation report. |
| `README_INSPECT.md` | Inspect-specific loading and execution instructions aligned with the TARA Week 10 / ARENA Chapter 3.3 workflow. |
| `ARENA_INSPECT_ALIGNMENT.md` | Mapping from Week 10 Inspect principles to the revised dataset object shape. |
| `data/inspect_samples_*.jsonl` | Inspect-ready raw records with `id`, `input`, `target`, and `metadata`. |
| `inspect_eval/pilot_control_task.py` | Inspect task definition, `record_to_sample`, dataset loader, and deterministic scorers. |
| `inspect_ready_validation_report.md` | Validation report, including Inspect CLI smoke-test status. |
| `ARENA_3_2_GAP_ASSESSMENT.md` | Assessment of alignment with the ARENA Chapter 3.2 dataset-generation syllabus. |
| `generation/` | Seed manifest, generation protocol, dataset quality rubric, audit/admission log, and duplicate/distribution checks for Chapter 3.2-style dataset generation discipline. |

## Split policy

The split is locked from Day 1 of Week 12. Odd-numbered cases are assigned to `dev`; even-numbered cases are assigned to `test`. This yields a 50/50 split with five development and five test cases in each scenario family.

## Scoring intent

Each case carries a gold decision, a gold escalation choice, applicability tags, an authority-structure specification, and rubric annotations for the five planned behavioural axes: correctness, calibration, escalation, authority-respect, and COLREGs/ROE rule-following.

## Inspect-ready execution

The package now includes an Inspect-compatible layer following the Week 10 ARENA/TARA pattern of `Dataset + Solver + Scorers`. From this directory, the development split can be smoke-tested or run with:

```bash
pip install -r requirements-inspect.txt
inspect eval inspect_eval/pilot_control_task.py@pilot_control --model openai/gpt-4o-mini --log-dir ./logs -T split=dev
```

The `record_to_sample` function in `inspect_eval/pilot_control_task.py` converts each raw JSONL line into an Inspect `Sample` with chat input, JSON-encoded target labels, and full metadata for filtering and scoring.

## ARENA Chapter 3.2 dataset-generation alignment

The `generation/` directory records the dataset-generation discipline expected by the ARENA Chapter 3.2 syllabus: seed provenance, a structured-output protocol, an admission rubric, an audit/rejection log format, and duplicate/distribution checks. The package intentionally keeps forty high-context behavioural cases rather than the syllabus exercise's approximate 300 MCQ target, because the project scope pre-registers a forty-case maritime safety benchmark with a possible scale-up to sixty cases if the Week-12 audit finds seed noise.
