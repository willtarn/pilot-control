# Current Dataset vs Inspect Sample Comparison

Total current cases: **40**.
Cases missing the current rich-case schema: **0**.
Cases already shaped as raw Inspect records with `id`, `input`, `target`, and `metadata`: **0**.

## Finding

The existing dataset contains the right benchmark information, but it is not yet in the most direct Inspect-ready record shape. The current top-level fields are rich authoring fields, while the Week 10 slides expect raw records to be converted into `Sample(input=..., target=..., metadata=...)` through `record_to_sample`.

## Required transformation

| Inspect concept | Current source field | Revised representation |
|---|---|---|
| Sample ID | `case_id` | `id` and `metadata.case_id` |
| Input prompt | `scenario` plus context/authority fields | `input` chat messages with system and user roles |
| Target answer | `gold_decision` and `gold_escalation` | `target` object/string containing the gold labels and required output schema |
| Metadata | scenario family, split, tags, rubric, tools, audit notes | `metadata` object preserving all scoring/filtering fields |
| Choices | `candidate_actions` | metadata only for behavioural free response; optional MCQ layer can later use `choices` with A/B/C targets |

The revised package should keep the rich source dataset, but add `data/inspect_samples_all.jsonl`, `data/inspect_samples_dev.jsonl`, and `data/inspect_samples_test.jsonl`, plus Python task files implementing `record_to_sample`, task constructors, and custom scorers.
