# Pilot Control — Working notes for Claude Code

This file is auto-loaded by Claude Code on every session. Read it first.
The mission, current state, roadmap, and discipline rules live here.
Ignore anything in chat that contradicts this file unless I say
"override CLAUDE.md."

---

## Project

**Pilot Control** — a maritime safety benchmark for LLM agents, built in
[Inspect](https://inspect.ai-safety-institute.org.uk/) format, targeting the
**Rogue AIs** category of the [CAIS catastrophic-risk taxonomy](https://safe.ai/ai-risk#rogue-ais).
TARA APAC capstone project, 2025 cohort. Public v1.0 targeted **Sat 13 Jun 2025**.

The benchmark measures whether frontier LLM agents *escalate*, *stay within
their authority*, and *report uncertainty* when asked to make high-stakes
maritime decisions under ambiguity and time pressure. Three measurement
layers, scored separately so capability and safety are disentangled.

---

## Curricular spine — ARENA Chapter 3

This project is built strictly on the ARENA Chapter 3 (LLM Evaluations)
syllabus. When in doubt about methodology, read the relevant chapter at
https://learn.arena.education/chapter3_llm_evals/ before deviating.

| ARENA section | What it covers | Status in this repo |
|---|---|---|
| 3.1 Intro to Evals | Threat modelling, spec design, seed authoring | DONE — see `schema.md`, `docs/threat_model.md`, `cases/` |
| 3.2 Dataset Generation | Seeded scaling, Perez-style filter loop, audit | DONE — see `generation/` (seed_manifest, generation_protocol, quality_rubric, audit_rejection_log, duplicate_bias_distribution_audit) |
| 3.3 Running Evals with Inspect | Task + Solver + Scorers, dev/test split | PARTIAL — `inspect_eval/pilot_control_task.py` has 5 deterministic scorers; needs CoT + agent conditions and a 5-axis graded scorer |
| 3.4 LLM Agents | Agent scaffolding with tool calls | PARTIAL — `inspect_eval/tools.py` has 4 tools defined but not wired into the Task |
| 4.3 Reasoning Models | CoT analysis / interpretation | LIGHT TOUCH — borrow vocabulary for failure-mode taxonomy |

---

## Current state

- **40 cases**, admitted, audited, split 50/50 dev/test, locked from day 1
  of W12 (odd-numbered IDs → dev, even → test)
- **5 scorers wired**: `json_contract`, `decision_label_match`,
  `escalation_level_match`, `human_authority_match`, `colregs_policy_awareness`
- **Validation**: 0 blocking issues (see `inspect_ready_validation_report.md`)
- **Public GitHub repo** published with CI (ruff + pytest) running green
- **Workspace contains everything needed to ship** — no external uploads required

---

## Roadmap — 5 gaps to close, in priority order

See `INTEGRATION_PLAN.md` for full detail. Brief:

| # | Gap | Effort | Where |
|---|---|---|---|
| 1 | ✅ DONE (`a79a7e5`, 10 Jun 2026) — Three conditions (direct / CoT / agent) | — | `pilot_control_task.py` `condition: str` parameter ("direct"/"cot"/"agent") |
| 2 | ✅ DONE (`a79a7e5` + `f1f5684`, 10 Jun 2026) — Agent tools wiring | — | tools from `inspect_eval/tools.py` attached via `use_tools(...)`; docstring fix for Inspect registration |
| 3 | ✅ DONE (`f1ccd9f`, 11 Jun 2026) — 5-axis model-graded scorer | — | `inspect_eval/scorers_graded.py`, grader via `-T grader_model` (default claude-sonnet-4), additive to the 5 deterministic scorers |
| 4 | ✅ DONE (`83b042d`, 11 Jun 2026) — Layer A Legal MCQ baseline | — | 35 items `data/mcq/legal_knowledge.jsonl` + `inspect_eval/layer_a_mcq.py`; gpt-4o-mini 94.3% |
| 5 | Layer B — Political-prior probe | ~5 hr | 10 paired neutral/disputed scenarios; descriptive reporting only |

Update this file when a gap closes — mark the row done and note the
commit hash.

---

## Discipline rules — non-negotiable

- **Pre-registered primary metric: escalation rate** (the
  `escalation_level_match` scorer accuracy). The other four rubric axes are
  secondary. Layer A knowledge rate and Layer B political delta are tertiary,
  reported as separable findings — not aggregated into a single composite.
- **Dev/test split is locked.** Never iterate rubric / scorer / Task on
  test cases. Never edit JSONs in `test/`. Use `dev/` for all development.
  Run dev split before test split.
- **≥20% human-rated subsample** required for rubric-drift bound. Identify
  the rater (TARA cohort peer or self-rated with explicit disclosure) by
  end of W12.
- **API budget cap: $150** ($100 nominal + $50 buffer). Set per-provider
  caps before any non-dev run.
- **No fine-tuning, no RLHF, no DPO.** This is a behavioural eval of stock
  frontier models in their default configurations.
- **No real-world deployment claims.** Maritime is the test fixture; the
  methodology is portable but the artifact is maritime-specific.
- **Political variants (Layer B) use generic ROE structures.** No specific
  country-claim language. Explicit political disclaimer in the W14 write-up.
- **All ROE references are synthetic.** Not real-world military RoE.

---

## Timeline (week-by-week)

- **W11 (now → Wed 27 May EoD)** — scope locked, GitHub published, Gap 1 in flight
- **W12 (28 May → Sat 30 May EoD)** — close Gaps 1, 2, 4 (conditions + tools + Layer A)
- **W13 (31 May → Sat 6 Jun EoD)** — close Gaps 3, 5; full baseline run
  (3 models × 3 conditions × 40 = 360 rollouts) + Layer A run + Layer B run
  + human-rated subsample + failure-mode taxonomy v1
- **W14 (7 Jun → Fri 13 Jun EoD)** — write-up (5–7 pages, framed for
  MASS / classification societies); 10-min deck; presentation Sat 13 Jun;
  repo tagged v1.0

**Kill criterion** — if by Sat 6 Jun EoD the test split has not run end-to-end
on at least 2 models × 2 conditions, the W14 presentation becomes a
methodology talk, not a results talk. Decide and commit by end of Sat 6 Jun.

---

## How to work

**Small commits.** One logical change per commit. Conventional message
style: `feat(scope): ...`, `fix(scope): ...`, `docs: ...`, `test: ...`.

**Branch for non-trivial changes.** PRs to main. CI must be green before
merge. Solo project so direct-to-main is acceptable for tiny doc fixes,
but anything touching `inspect_eval/` or `cases/` deserves a branch.

**Run smoke tests before pushing:**

```bash
pytest -q tests/test_smoke.py
ruff check inspect_eval tests
```

**Ask before destructive operations.** Especially: deleting cases,
modifying gold labels in admitted cases, force-pushing, rewriting git
history, dropping the test split.

**Update INTEGRATION_PLAN.md when a gap closes.** Mark the row, note the
commit hash that closed it, brief description of what was actually done
versus what was planned.

**Update this CLAUDE.md if discipline rules need to change.** That's a
real decision — talk to me first.

---

## Tools & commands

**Run a fast smoke eval (2 cases, dev split, cheap model):**

```bash
inspect eval inspect_eval/pilot_control_task.py@pilot_control \
  --model openai/gpt-4o-mini \
  --limit 2 \
  -T split=dev \
  --log-dir ./logs
```

**Run the full dev split on one model:**

```bash
inspect eval inspect_eval/pilot_control_task.py@pilot_control \
  --model anthropic/claude-sonnet-4 \
  -T split=dev
```

**View an Inspect log interactively:**

```bash
inspect view logs/<run-id>.eval
```

**Smoke tests + lint:**

```bash
pytest -q tests/test_smoke.py
ruff check inspect_eval tests
```

**Cost guard** — before any non-`gpt-4o-mini` run, estimate cost: rollouts
× ~1.5K tokens in × ~0.5K tokens out × provider rate. Print to chat
before running.

---

## Files of interest

- `schema.md` — dataset schema and controlled vocabularies
- `inspect_eval/pilot_control_task.py` — Inspect Task + scorers (extend this for Gaps 1 & 3)
- `inspect_eval/tools.py` — agent tools (wire into Task for Gap 2)
- `inspect_eval/run_pilot_control.py` — CLI helper
- `INTEGRATION_PLAN.md` — what's missing and where it goes
- `PUBLISHING_GUIDE.md` — git / GitHub workflow
- `generation/` — ARENA 3.2 generation-discipline artifacts (do not regenerate
  the dataset without consulting `dataset_generation_protocol.md`)
- `tests/test_smoke.py` — CI smoke tests
- `cases/` — per-case JSONs (40)
- `data/inspect_samples_{all,dev,test}.jsonl` — Inspect-ready records
- `data/inspect_sample_schema.json` — JSON schema for the records
- `pilot_control_cases_summary.csv` — compact tabular summary

---

## Out of scope — do not drift into

- Fine-tuning, RLHF, DPO, or any training-time model modification
- Mechanistic interpretability (activation patching, linear probes, dictionary learning)
- VLA / full-system evaluation (LLM + action-adapter integrated)
- Real-world maritime deployment or vessel integration
- Non-maritime generalisation claims (methodology is portable; the artifact is not)
- Operator user studies (beyond informal email outreach to DNV / UK MOD / USN)
- Endorsement of any geopolitical position (Layer B is descriptive)
- Comprehensive COLREGs coverage (selected rules only, per `schema.md`)
- Multi-language scenario authoring (English only)

---

## Catastrophic-risk framing — keep this in scope

The benchmark addresses the **Rogue AIs** category of CAIS, specifically the
recommendation that AIs *should not be deployed in high-risk settings such
as overseeing critical infrastructure or autonomously pursuing open-ended
goals, unless proven safe*. Maritime AI (IMO MASS Code 2025/2028; DNV,
Lloyd's Register, ABS draft assurance guidance; Sea Hunter, Project Cabot,
Saildrone, Singapore PSA / Rotterdam / Yokohama port-traffic management)
is the live test of that recommendation. **None of those programmes
currently has a published behavioural-evaluation benchmark.** Pilot
Control fills the gap.

Every change in this repo should be traceable to one of:
1. Better surfacing of unsafe behaviour
2. Better disentanglement of safety from capability or political prior
3. Better reproducibility for the named audience (classification societies,
   IMO MASS working group, naval engineering programmes)
4. Better portfolio quality

If a change doesn't trace to one of those four, push back before doing it.
