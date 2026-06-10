# ARENA Chapter 3.2 Duplicate, Bias, and Distribution Audit

This audit records the checks expected by the dataset-generation syllabus: distribution checks, duplicate or near-duplicate review, and potential answer/label imbalance review. The Pilot Control dataset is not an MCQ dataset, so answer-order bias is not applicable to the behavioural cases; if the Layer A MCQ baseline is added, it should include separate MCQ choice-order randomization and answer-letter distribution checks.

## Family and split distribution

| Scenario family | Dev | Test | Total |
|---|---:|---:|---:|
| anomaly_triage | 5 | 5 | 10 |
| autonomous_surface_vessel_exception_handling | 5 | 5 | 10 |
| incident_escalation | 5 | 5 | 10 |
| maintenance_deferral | 5 | 5 | 10 |

## Gold decision distribution by family

### anomaly_triage

| Gold decision label | Count |
|---|---:|
| investigate_before_action | 9 |
| escalate_before_action | 1 |

### autonomous_surface_vessel_exception_handling

| Gold decision label | Count |
|---|---:|
| escalate_before_action | 5 |
| emergency_manoeuvre_required | 2 |
| slow_or_hold_position | 2 |
| investigate_before_action | 1 |

### incident_escalation

| Gold decision label | Count |
|---|---:|
| escalate_before_action | 8 |
| investigate_before_action | 1 |
| emergency_manoeuvre_required | 1 |

### maintenance_deferral

| Gold decision label | Count |
|---|---:|
| defer_or_abort_operation | 5 |
| investigate_before_action | 3 |
| slow_or_hold_position | 1 |
| escalate_before_action | 1 |

## Gold escalation distribution by family

### anomaly_triage

| Gold escalation level | Count |
|---|---:|
| master | 4 |
| watch_officer | 3 |
| remote_operations_supervisor | 2 |
| chief_engineer | 1 |

### autonomous_surface_vessel_exception_handling

| Gold escalation level | Count |
|---|---:|
| remote_operations_supervisor | 10 |

### incident_escalation

| Gold escalation level | Count |
|---|---:|
| master | 7 |
| watch_officer | 2 |
| port_authority | 1 |

### maintenance_deferral

| Gold escalation level | Count |
|---|---:|
| master | 5 |
| company_dpa | 3 |
| watch_officer | 1 |
| chief_engineer | 1 |

## COLREGs tag coverage

| COLREGs tag | Count |
|---|---:|
| Rule 5 | 29 |
| Rule 7 | 17 |
| Rule 8 | 14 |
| Rule 6 | 13 |
| none | 10 |
| Rule 10 | 4 |
| Rule 15 | 3 |
| Rule 17 | 2 |
| Rule 9 | 2 |
| Rule 14 | 1 |

## Near-duplicate screen

The lexical near-duplicate screen flagged the following pairs for human review. These are not automatically rejected because scenario families intentionally share maritime vocabulary such as traffic, escalation, and COLREGs.

| Case A | Case B | Jaccard token overlap | Family A | Family B | Human review disposition |
|---|---|---:|---|---|---|
| PC-AT-02 | PC-AT-05 | 0.336 | anomaly_triage | anomaly_triage | Retain both. PC-AT-02 tests navigation-sensor disagreement near shoal water; PC-AT-05 tests unidentified small-craft/security ambiguity. The lexical overlap comes from shared anomaly-triage and coastal-navigation vocabulary, not duplicated decision content. |

## Bias/order note

Because these behavioural cases ask for structured free-response JSON rather than choosing from randomized answer options, MCQ answer-order bias is not applicable here. Candidate actions are included for scoring context and human readability, but they are not passed to Inspect as `choices`. The future Layer A legal-knowledge MCQ baseline should separately use capital-letter targets and shuffled choices, as expected by the Inspect MCQ workflow.
