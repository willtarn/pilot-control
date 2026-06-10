# Pilot Control Maritime Safety Benchmark Dataset — Release Notes

This release contains **40 structured behavioural-evaluation scenarios** for the project **Pilot Control: A Maritime Safety Benchmark for LLM Agents**. The dataset is organized around four scenario families requested in the scoping template: **maintenance deferral**, **anomaly triage**, **incident escalation**, and **autonomous-surface-vessel exception handling**. Each family contains ten cases, producing a balanced forty-case benchmark.

## Dataset composition

| Scenario family | Total cases | Dev | Test |
|---|---:|---:|---:|
| Maintenance deferral | 10 | 5 | 5 |
| Anomaly triage | 10 | 5 | 5 |
| Incident escalation | 10 | 5 | 5 |
| Autonomous-surface-vessel exception handling | 10 | 5 | 5 |
| **Total** | **40** | **20** | **20** |

The split is locked from Day 1 of Week 12 using a deterministic policy: odd-numbered cases are assigned to `dev` and even-numbered cases are assigned to `test`. This gives each scenario family exactly five development cases and five held-out test cases.

## Included annotations

Every case includes the fields required by the scoping brief: a **gold decision**, a **gold escalation choice**, **COLREGs/ROE applicability tags**, an **authority-structure specification**, and **rubric annotations**. Rubric annotations cover the five planned behavioural axes: correctness, calibration, escalation, authority-respect, and COLREGs/ROE rule-following.

| Annotation class | Implementation in dataset |
|---|---|
| Gold decision | `gold_decision.decision_label`, `decision_text`, `rationale`, `acceptable_alternatives`, and `unacceptable_actions`. |
| Gold escalation | `gold_escalation.level`, `recipients`, `urgency`, `request_human_authority_expected`, and `escalation_text`. |
| Applicability tags | `applicability_tags.colregs`, `applicability_tags.unclos`, and `applicability_tags.roe_policy`, stored as arrays. |
| Authority structure | `authority_structure.operating_mode`, `on_scene_authority`, `remote_authority`, `delegated_limits`, `approvals_required`, and `prohibited_autonomous_actions`. |
| Rubric annotations | Per-axis `full_credit`, `partial_credit`, `no_credit`, and `key_observables`. |

## Validation status

The final dataset passes schema validation with **0 blocking issues**. The content audit confirms that all forty cases contain the five rubric axes, all forty require human-authority escalation or review in the gold label, and the dev/test split is balanced by family.

## Reference grounding

The legal and navigational tags are grounded in public references. The IMO COLREGs convention page explains the structure and selected requirements of the collision-prevention rules, including Rules 5, 6, 7, and 8.[^1] The consolidated COLREGs reference used for exact case grounding gives the selected rule text for Rules 5, 6, 7, 8, 14, 15, and 17.[^2] UNCLOS Articles 17–24 are used only for innocent-passage and coastal-state-law context, including the right of innocent passage, the definition of innocent passage, and coastal-state laws relating to navigation safety and maritime traffic.[^3]

The ROE/policy fields are deliberately generic and synthetic. They are benchmark constraints for testing authority-respect and escalation behaviour; they are **not** real military rules of engagement.

[^1]: International Maritime Organization, [Convention on the International Regulations for Preventing Collisions at Sea, 1972 (COLREGs)](https://www.imo.org/en/about/conventions/pages/colreg.aspx).
[^2]: Icelandic Transport Authority, [COLREGs Consolidated 2018 PDF](https://www.samgongustofa.is/media/log-og-reglur/COLREG-Consolidated-2018.pdf).
[^3]: United Nations, [United Nations Convention on the Law of the Sea, Part II](https://www.un.org/depts/los/convention_agreements/texts/unclos/part2.htm).
