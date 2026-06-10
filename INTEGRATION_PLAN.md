# Integration plan — Pilot Control benchmark

> What this folder already contains, what's missing for the full Pilot
> Control benchmark, and where each remaining piece goes.

## What this folder already contains (W12 deliverable — complete)

The dataset in this folder is **substantively the Week-12 deliverable**: 40
admitted behavioural-evaluation cases across the four scenario families, a
locked dev/test split, Inspect-ready JSONL records, an Inspect `Task` with
five deterministic scorers, full ARENA Chapter 3.2 generation-discipline
artifacts, and a clean validation report (0 blocking issues).

Concretely:

| Asset | Where | Status |
|---|---|---|
| 40 cases, JSON, one per file | `cases/`, `dev/`, `test/` | Complete, audited, admitted |
| Aggregated case files | `pilot_control_cases_*.json`, `*.jsonl`, `*.csv` | Complete |
| Inspect-ready records | `data/inspect_samples_{all,dev,test}.jsonl` | Complete, schema-validated |
| Inspect `Task` + scorers | `inspect_eval/pilot_control_task.py` | Complete: `json_contract`, `decision_label_match`, `escalation_level_match`, `human_authority_match`, `colregs_policy_awareness` |
| Run helper | `inspect_eval/run_pilot_control.py` | Complete |
| Schema and controlled vocabularies | `schema.md` | Complete |
| Generation provenance | `generation/seed_manifest.json`, `dataset_generation_protocol.md`, `question_quality_rubric.md`, `audit_rejection_log.csv`, `duplicate_bias_distribution_audit.md` | Complete |
| Research notes | `research_notes.md` | Complete |
| Validation reports | `validation_report.md`, `inspect_ready_validation_report.md`, `content_audit.md` | Complete |

The dataset is ready to run. The smoke-test command in `README_INSPECT.md`
should produce valid scored output today.

---

## What's still missing for the full benchmark

Five gaps, in priority order. Most have low build cost; all build on what's
here.

### Gap 1 — Three conditions (direct / CoT / agent) — ✅ DONE

> **Closed 10 Jun 2026**, commit `a79a7e5` (`feat(task): add direct/cot/agent
> conditions`), plus `f1f5684` (`fix(tools): add missing execute() docstrings`).
> `pilot_control()` now takes `condition: str = "direct"`; invalid values raise
> `ValueError`. Verified: 2-case dev smoke evals green in all three conditions
> (gpt-4o-mini); agent log shows 5 tool calls across 2 samples, including
> `request_human_authority`.
>
> **Deviations from plan.** (1) Used a plain `system_message(COT_PROMPT)`
> appended after the per-case system prompt rather than Inspect's
> `chain_of_thought()` helper — the dataset embeds its own system prompt per
> sample, and `chain_of_thought()` rewrites the user prompt, which would touch
> locked case content. (2) Task name gains a `_{condition}` suffix for non-direct
> runs (e.g. `pilot_control_dev_agent`) so W13 baseline logs are distinguishable;
> direct names are unchanged for backward compatibility. (3) Two tools had
> missing inner docstrings and failed Inspect registration at runtime — fixed in
> `f1f5684`; this also closed the remainder of Gap 2 (the wiring) in the same
> pass.

**Current state.** The `pilot_control` Task runs a single solver: `generate()`.
This is the **direct** condition only.

**What's needed.** Two additional conditions:

- **CoT** — same solver chain plus a "think step by step" `system_message`
  before `generate()`. Or use Inspect's `chain_of_thought()` solver helper.
- **Agent-with-tools** — `use_tools([...])` with four tools (see Gap 2),
  then `generate()`. The agent variant is the central H1 condition — does
  scaffolding change escalation rate?

**Where it goes.** Extend `inspect_eval/pilot_control_task.py` with a
`condition` parameter:

```python
@task
def pilot_control(split: str = "all", scenario_family: str | None = None,
                  condition: str = "direct") -> Task:
    solver = [system_message(SYSTEM_PROMPT)]
    if condition == "cot":
        solver.append(chain_of_thought())
    elif condition == "agent":
        solver.append(use_tools([consult_roe(), check_weather(),
                                 request_human_authority(), log_decision()]))
    solver.append(generate())
    return Task(...)
```

**Effort.** ~3 hours including a smoke run on dev.

### Gap 2 — Agent tools — ✅ DONE

> **Closed 10 Jun 2026.** `inspect_eval/tools.py` already contained the four
> tools; commit `a79a7e5` wired them into the agent condition via
> `use_tools(...)` and `f1f5684` fixed the two missing `execute()` docstrings
> that Inspect requires for tool registration.

**Current state.** Per-case `tool_expectations` blocks reference four tools
(`consult_ROE`, `check_weather`, `request_human_authority`, `log_decision`)
with `expected`/`optional`/`not_expected` calls. The tool implementations
live in `inspect_eval/tools.py`.

**What's there.** Four Inspect `@tool` functions, all log-only with no
real-world side effects:

- `consult_roe(scenario_id)` — returns the relevant ROE / COLREGs excerpt.
- `check_weather(location, time_utc)` — returns weather string.
- `request_human_authority(decision, justification)` — always returns
  "request submitted, no response received" (operator-unreachable
  simulation; the model's behaviour after this response is the load-bearing
  observation).
- `log_decision(decision, rationale)` — append-only log confirmation.

**Where it lives.** `inspect_eval/tools.py`, attached to the agent condition
in `inspect_eval/pilot_control_task.py`.

### Gap 3 — 5-axis model-graded scorer wired to the rubric annotations — ✅ DONE

> **Closed 11 Jun 2026**, commits `f1ccd9f` (`feat(scorer)`) + `b268392`
> (`test(smoke)`). `inspect_eval/scorers_graded.py` adds `five_axis_graded()`:
> grader configurable via `-T grader_model=...` (default
> `anthropic/claude-sonnet-4`), same-model subject/grader rejected at grading
> time (compared ignoring provider/router prefixes), 0/1/2 per axis + one-line
> justification in Score.metadata, Score.value = normalised total (0..1,
> `mean()` metric). Wired into the Task additively — all 5 deterministic
> scorers retained; `escalation_level_match` remains the pre-registered
> primary metric and the graded escalation axis is documented as secondary.
> Unparseable grader output is retried once then scored 0 with a
> `grading_failed` flag.
>
> **Verified.** 2-case dev smoke (subject gpt-4o-mini, grader
> openrouter/anthropic/claude-sonnet-4): both samples graded, no parse
> failures, per-axis justifications grounded in the responses. Grading cost
> ~$0.03.
>
> **Deviation / finding.** The smoke run exposed that subjects emit free-form
> `decision_label` values (e.g. `alter_course_to_avoid_collision`) instead of
> the controlled vocabulary, so `decision_label_match` reads 0 even when the
> graded axes award full credit. This is a JSON-contract/vocabulary issue, not
> a safety failure — decide before the W13 baseline whether the system prompt
> should enumerate the allowed labels (case content is locked; scorer changes
> are ask-first).
>
> TODO(W13): bound rubric drift with the ≥20% human-rated subsample before
> trusting graded axes in the write-up.

**Current state.** Each case has rich `rubric_annotations` with
`full_credit`/`partial_credit`/`no_credit`/`key_observables` per axis. The
wired Inspect scorers are all **deterministic** — they check JSON contract,
decision label, escalation level, human-authority match, and a lightweight
tag-awareness proxy for rule-following.

**Gap.** No scorer currently uses the per-case rubric annotations for the
five qualitative axes (correctness, calibration, escalation,
authority-respect, COLREGs/ROE rule-following). The submission's primary
metric (escalation rate) is partially covered by `escalation_level_match`,
but the other four axes need a graded scorer to consume the per-case rubric.

**What's needed.** A `five_axis_graded_scorer()` that:

1. Injects the per-case `rubric_annotations` into a model-graded prompt.
2. Returns a 0/1/2 score per axis, plus a one-line justification.
3. Aggregates to a JSON dict matching the project's reporting structure.

The grading model must be different from the subject model. Bound rubric
drift with the ≥20% human-rated subsample.

**Where it goes.** Extend `inspect_eval/pilot_control_task.py` with a new
scorer or add `inspect_eval/scorers_graded.py`.

**Effort.** ~5 hours including a small calibration pass on the dev split.

### Gap 4 — Layer A (legal-knowledge MCQ baseline)

**Current state.** Not in this folder. Mentioned in the submission as a
separate measurement layer; needed to disentangle knowledge gaps from safety
failures.

**What's needed.**

- 30–50 MCQ items covering COLREGs (Rules 5, 6, 7, 8, 14, 15, 17), UNCLOS
  Articles 17–32 on innocent passage, and basic port-state / flag-state
  authority structure.
- A separate Inspect `Task` that runs MCQ with deterministic scoring.
- Conditional reporting in the Layer C results: "of cases where the model
  passes Layer A, X% pass the safety rubric."

**Where it goes.**

- Data: `data/mcq/legal_knowledge.jsonl` (new directory).
- Task: `inspect_eval/layer_a_mcq.py`.

**Effort.** ~3 hours (authoring + scaffolding).

### Gap 5 — Layer B (political-prior probe)

**Current state.** Not in this folder. Submission commits to 10 paired
geographic-variant scenarios (neutral vs disputed waters), descriptive
reporting only.

**What's needed.**

- 10 paired scenarios — select 10 cases from `dev/` and re-author the
  geographic descriptor for each, holding everything else constant.
- Scenarios use generic ROE structures; explicit political disclaimer in
  the write-up.
- Separate Inspect `Task` that runs the pair and reports behaviour delta.

**Where it goes.**

- Data: `data/scenarios/political_variants/{neutral,disputed}.jsonl`.
- Task: `inspect_eval/layer_b_political.py`.

**Effort.** ~5 hours including the ethical-framing review of the disputed
variants.

---

## What's missing for the GitHub repo / portfolio piece

The dataset is a research package; turning it into a portfolio repo needs:

- `README.md` at repo root (the dataset has good `README.md` already, but it's
  inward-facing; the repo README should be a portfolio piece for someone
  visiting cold).
- `LICENSE` (MIT recommended).
- `pyproject.toml` for `pip install -e .`.
- `.gitignore` excluding `logs/`, `.env`, and `__pycache__/`.
- `CITATION.cff` for academic citation.
- `.github/workflows/ci.yml` running `ruff` + `pytest` on every PR.
- `tests/test_smoke.py` verifying the package imports and the dataset loads.

These are all in the `pilot-control-starter` scaffold previously delivered
and can be copied over directly. They are independent of the dataset.

---

## Suggested W11–W14 working order

| Week | Action |
|---|---|
| **W11 lock-in (by Wed 27 May)** | Decide primary metric encoding (the dataset's per-case `gold_decision` and `decision_label_match` scorer already nail this — primary metric = `escalation_level_match` accuracy). Confirm 3 conditions × 3 models × 40 cases scope. Apply portfolio-repo scaffolding (README, LICENSE, pyproject, CI). Send the two cold emails. |
| **W12 (now → 30 May)** | Mostly done. **Remaining:** implement Gap 1 (CoT + agent conditions), Gap 2 (agent tools), Gap 4 (Layer A MCQ — author and scaffold). |
| **W13 (31 May → 6 Jun)** | Implement Gap 3 (5-axis graded scorer). Author Gap 5 (Layer B paired variants). Run baseline: 3 × 3 × 40 = 360 main rollouts + 120 MCQ + 180 Layer-B variants. Human-rated subsample with cohort peer. Failure-mode taxonomy v1. |
| **W14 (7 → 13 Jun)** | Write-up. Results notebook. Presentation. Repo v1.0 tag. Optional LessWrong post. |

## Cost check

The dataset's `pilot_control_cases_summary.csv` shows 40 cases. At three
conditions × three models, the main run is ~360 rollouts; add ~120 MCQ
and ~180 Layer-B variants for ~660 LLM calls before retries. At realistic
frontier-API rates this lands ~$80–95. Honour the **$150** cap from the
scoping doc ($100 nominal + $50 buffer); set per-provider usage caps.

## Effort total

Roughly **18–20 hours** of remaining build across the five gaps, comfortably
within the W12–W13 budget. The largest single piece is Gap 3 (the graded
scorer); the cheapest with the highest signal is Gap 1 (adding the two
conditions to the existing Task).
