# Pilot Control Dataset Validation Report

Total cases: **40**.

| Scenario family | Total | Dev | Test |
|---|---:|---:|---:|
| anomaly_triage | 10 | 5 | 5 |
| autonomous_surface_vessel_exception_handling | 10 | 5 | 5 |
| incident_escalation | 10 | 5 | 5 |
| maintenance_deferral | 10 | 5 | 5 |

## Schema validation

Validation found **0 blocking schema issues**. All cases include the required top-level fields, authority structures, gold labels, rubric axes, tool expectations, and admission notes.

## Split lock

The split is locked by case number: odd-numbered cases are `dev`, even-numbered cases are `test`. Each scenario family contributes five development cases and five test cases.
