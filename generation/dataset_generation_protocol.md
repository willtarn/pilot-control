# ARENA Chapter 3.2 Dataset-Generation Protocol for Pilot Control

This protocol makes the Pilot Control dataset auditable under the ARENA Chapter 3.2 workflow. The Chapter 3.2 syllabus emphasizes using LLMs to generate and refine evaluation datasets, applying structured output schemas, scoring generated items with rubrics, filtering flawed items, manually checking quality, reviewing distribution and duplicate risks, and then passing the resulting dataset into Chapter 3.3 model evaluation.

## Scope adaptation

The ARENA exercise target is approximately 300 MCQ questions, but Pilot Control has a pre-registered project scope of forty structured maritime behavioural cases across four scenario families. This is an intentional scope adaptation. The dataset is therefore not a direct MCQ exercise clone; it applies the same generation and quality-control principles to a smaller, higher-context behavioural safety benchmark.

## Generation loop

| Step | Pilot Control implementation |
|---|---|
| Seed design | `generation/seed_manifest.json` records the forty seed prompts, split assignments, families, and final case titles. |
| Structured generation | Each final case follows the rich JSON schema in `schema.md`, including gold decision, gold escalation, tags, authority structure, and rubric annotations. |
| Scaling | Cases are distributed as ten per family, with five development and five test samples per family. The project scope permits scaling to sixty cases if seed noise proves high. |
| Quality rubric | `generation/question_quality_rubric.md` defines admission criteria for relevance, realism, format validity, authority structure, gold labels, rule tags, and duplicate risk. |
| Filtering and admission | `generation/audit_rejection_log.csv` records admission decisions and is structured to include rejected generations if future audit passes reject cases. |
| Distribution review | `generation/duplicate_bias_distribution_audit.md` records family/split balance, gold-label distribution, COLREGs tag coverage, near-duplicate review, and the MCQ answer-order note. |
| Evaluation handoff | `data/inspect_samples_*.jsonl` and `inspect_eval/pilot_control_task.py` hand the dataset to Chapter 3.3-style Inspect evaluation. |

## Structured output contract

The rich case object contains: `case_id`, `split`, `scenario_family`, `title`, `operational_context`, `authority_structure`, `scenario`, `candidate_actions`, `gold_decision`, `gold_escalation`, `applicability_tags`, `rubric_annotations`, `failure_modes_targeted`, `tool_expectations`, and `audit_notes`. The Inspect-facing object contains: `id`, `input`, `target`, and `metadata`. This two-layer design keeps the dataset readable as a research artifact while also making it runnable as an Inspect dataset.

## Future scaling guidance

If a Week-12 audit finds seed noise, add new candidates by family in increments of five, run them through the same rubric, append rejected cases to the audit log, and preserve the held-out test split. For an MCQ Layer A baseline, use a separate file with Inspect `choices` and capital-letter targets, then run answer-order balancing and choice shuffling separately from these behavioural cases.
