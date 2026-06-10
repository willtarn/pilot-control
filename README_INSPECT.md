# Inspect-Ready Pilot Control Dataset

This package adds an ARENA/TARA Week 10 compatible Inspect layer on top of the rich Pilot Control case objects. The original case files remain available under `cases/`, while the files under `data/` are normalized raw records intended to be converted into Inspect `Sample` objects by `inspect_eval/pilot_control_task.py`.

## Why this format matches the Week 10 Inspect pattern

The Week 10 slides define an Inspect task as a combination of a **Dataset**, a **Plan/Solver**, and **Scorers**. They also show that each raw record should be converted by `record_to_sample` into a `Sample` containing `input`, optional `choices`, a `target`, and `metadata`. This package follows that pattern directly: every JSONL line has `id`, `input`, `target`, and `metadata`, and `record_to_sample` maps those fields into `Sample(id=..., input=[ChatMessageSystem, ChatMessageUser], target=..., metadata=...)`.

| Inspect concept from Week 10 | Implemented file/field |
|---|---|
| Dataset as list of Sample questions | `data/inspect_samples_all.jsonl`, `data/inspect_samples_dev.jsonl`, `data/inspect_samples_test.jsonl` |
| `record_to_sample(record)` conversion | `inspect_eval/pilot_control_task.py` |
| System and user chat messages | `input.system` and `input.user` |
| Target answer for scoring | `target`, encoded as JSON by `record_to_sample` because Inspect `Sample.target` expects a string or list of strings |
| Metadata for parsing, filtering, and scoring | `metadata.scenario_family`, `metadata.split`, `metadata.applicability_tags`, `metadata.rubric_annotations`, and related fields |
| Solver plan | Default `generate()` solver in `pilot_control()`; this can be swapped for CoT, self-critique, or agent/tool solvers |
| Custom scorers | JSON contract, decision label match, escalation level match, human-authority match, and COLREGs/policy awareness scorers |

## Files added

| File | Purpose |
|---|---|
| `data/inspect_samples_all.jsonl` | All forty Inspect-ready behavioural samples. |
| `data/inspect_samples_dev.jsonl` | Twenty-sample development split. |
| `data/inspect_samples_test.jsonl` | Twenty-sample held-out test split. |
| `data/inspect_sample_schema.json` | Lightweight schema for the raw JSONL record shape. |
| `inspect_eval/pilot_control_task.py` | Inspect task, `record_to_sample`, dataset loader, and deterministic scorers. |
| `inspect_eval/run_pilot_control.py` | Optional Python runner around `inspect_ai.eval`. |
| `requirements-inspect.txt` | Minimal Inspect dependency file. |

## Example commands

From the `pilot_control_dataset` directory, install Inspect and run a smoke evaluation as follows:

```bash
pip install -r requirements-inspect.txt
inspect eval inspect_eval/pilot_control_task.py@pilot_control --model openai/gpt-4o-mini --log-dir ./logs -T split=dev
```

To run only one family on the test split, pass both task arguments:

```bash
inspect eval inspect_eval/pilot_control_task.py@pilot_control --model openai/gpt-4o-mini --log-dir ./logs -T split=test -T scenario_family=incident_escalation
```

The included task uses deterministic scorers for the structured output contract and several gold-label axes. It is intentionally compatible with later ARENA-style sweeps: the same JSONL samples can be reused with direct prompting, chain-of-thought prompting, self-critique, or an agent/tool plan without changing the held-out split.
