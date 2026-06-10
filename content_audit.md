# Pilot Control Dataset Content Audit

Total cases audited: **40**.

## Family and split balance

| Scenario family | Dev | Test | Total |
|---|---:|---:|---:|
| anomaly_triage | 5 | 5 | 10 |
| autonomous_surface_vessel_exception_handling | 5 | 5 | 10 |
| incident_escalation | 5 | 5 | 10 |
| maintenance_deferral | 5 | 5 | 10 |

## Gold decision distribution

| Decision label | Count |
|---|---:|
| escalate_before_action | 15 |
| investigate_before_action | 14 |
| defer_or_abort_operation | 5 |
| emergency_manoeuvre_required | 3 |
| slow_or_hold_position | 3 |

## Gold escalation distribution

| Escalation level | Count |
|---|---:|
| master | 16 |
| remote_operations_supervisor | 12 |
| watch_officer | 6 |
| company_dpa | 3 |
| chief_engineer | 2 |
| port_authority | 1 |

## Human authority expectation

| request_human_authority_expected | Count |
|---|---:|
| True | 40 |

## COLREGs tag distribution

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

## UNCLOS tag distribution

| UNCLOS tag | Count |
|---|---:|
| none | 28 |
| coastal_state_laws_article_21 | 7 |
| innocent_passage_article_19 | 4 |
| sea_lanes_tss_article_22 | 4 |
| innocent_passage_article_17 | 1 |
| passage_continuous_expeditious_article_18 | 1 |

## Generic ROE/policy tag distribution

| Policy tag | Count |
|---|---:|
| none | 26 |
| notify_chain_of_command | 11 |
| minimum_safe_action_only | 6 |
| generic_force_protection | 4 |
| no_use_of_force_without_authority | 3 |
| evidence_preservation | 2 |
| survey_or_intelligence_sensitive | 1 |

## Failure-mode target distribution

| Failure mode | Count |
|---|---:|
| under_escalation | 32 |
| mission_pressure_over_safety | 27 |
| overconfident_under_uncertainty | 16 |
| automation_bias | 14 |
| inappropriate_authority_assumption | 10 |
| rule_misapplication | 5 |
| political_or_security_overreach | 4 |

## Rubric axis coverage

| Rubric axis | Cases covered |
|---|---:|
| correctness | 40 |
| calibration | 40 |
| escalation | 40 |
| authority_respect | 40 |
| colregs_roe_rule_following | 40 |

## Quality warnings

No short-scenario or candidate-action coverage warnings were found.
