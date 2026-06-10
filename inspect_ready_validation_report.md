# Inspect-Ready Dataset Validation Report

Validated raw Inspect records: **40** all, **20** dev, and **20** test.

| Scenario family | Dev | Test | Total |
|---|---:|---:|---:|
| anomaly_triage | 5 | 5 | 10 |
| autonomous_surface_vessel_exception_handling | 5 | 5 | 10 |
| incident_escalation | 5 | 5 | 10 |
| maintenance_deferral | 5 | 5 | 10 |

## Checks performed

The validation checked JSONL parseability, required `id`/`input`/`target`/`metadata` fields, split disjointness, family balance, `record_to_sample` conversion, task import, and filtered task dataset lengths.

## Result

Validation found **0 blocking issues**. The dataset is shaped for Inspect loading through `record_to_sample` and supports split/family filtering for ARENA-style sweeps.
