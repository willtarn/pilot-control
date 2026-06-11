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

## Political probes (named-actor tier, quarantined)

`cases/political_probes/` contains a five-case named-actor extension of the
Layer B political-prior probe ("Layer B+"). Unlike Layer B, these cases name
specific coast guards, naval forces, and contested areas, each in a neutral
(NEU) variant plus one or two named-disputed variants. This tier sits
**entirely outside the locked main 40**: `split` is `"probe"`, nothing in it
contributes to the pre-registered primary metric, and all reporting is
descriptive and per-case (N=5 pairs — no significance tests).

**Disclaimer (binding, from `cases/political_probes/README.md`):** these
probes test behavioural consistency under a named-actor swap. They take no
position on: the sovereignty of any contested maritime feature or area; the
lawful scope of any specific coastal state's UNCLOS Article 234 application;
the legitimacy of any specific coast guard, naval force, or boarding party;
or the correct place-name for any contested archipelago. The **gold answer
is identical for every variant of every case** — the only measured quantity
is whether model behaviour shifts when the parties are named. None of the
probes ask any model to take a side; a model asked to adjudicate the
underlying political question should decline.

Generation: `generation/make_political_probes.py` (verbatim anchor
replacement, pair invariants enforced by `tests/test_political_probes_smoke.py`).
Runner: `inspect_eval/political_probes.py`. Results: section 7 of
`notebooks/01_results_analysis.ipynb` and `docs/failure_taxonomy.md` §6.

## Known caveats (read before citing results)

1. **Controlled-vocabulary drift.** Models frequently emit synonym strings
   for correct escalation roles (`roc_supervisor` for
   `remote_operations_supervisor`); the deterministic primary metric counts
   these as misses and understates true escalation agreement by roughly
   7–20 percentage points (exploratory bound in the results notebook, §6).
   The pre-registered metric is reported raw and unchanged.
2. **Graded axes are not yet human-validated.** The ≥20% human-rated
   subsample required to bound rubric drift has not been collected; treat
   model-graded axis scores as provisional.
3. **Timeline disclosure.** The project's pre-registered kill criterion
   (test split run end-to-end by 6 Jun 2026) was not met; the full baseline
   ran 10–11 Jun 2026. Results post-date the deadline the protocol set.
