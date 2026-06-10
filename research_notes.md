# Maritime Dataset Research Notes

## Source: IMO COLREGs convention page
URL: https://www.imo.org/en/about/conventions/pages/colreg.aspx

Key points extracted:

- The 1972 Convention on the International Regulations for Preventing Collisions at Sea (COLREGs) was adopted on 20 October 1972 and entered into force on 15 July 1977.
- COLREGs apply to all vessels on the high seas and connected waters navigable by seagoing vessels.
- The rules include 41 rules across General, Steering and Sailing, Lights and Shapes, Sound and Light Signals, Exemptions, and Verification sections.
- Rule 5 requires every vessel to maintain a proper look-out by sight, hearing, and all available means appropriate to the prevailing conditions, to fully appraise the situation and collision risk.
- Rule 6 requires every vessel to proceed at a safe speed at all times, considering the prevailing circumstances and conditions.
- Rule 7 requires the use of all available means to determine risk of collision and warns against assumptions based on scanty information, especially scanty radar information.
- Rule 8 covers action to avoid collision, emphasizing appropriate avoidance action when collision risk exists.
- Rule 9 and Rule 10 are relevant for narrow channels and traffic separation schemes, respectively, although the requested dataset pre-registers selected coverage mainly around Rules 5, 6, 7, 8, 14, 15, and 17.

## Source: UN UNCLOS search result and official page/PDF references
URLs found:
- https://www.un.org/depts/los/convention_agreements/texts/unclos/part2.htm
- https://www.un.org/depts/los/convention_agreements/texts/unclos/unclos_e.pdf

Key points for dataset design:

- UNCLOS Part II, Section 3 covers innocent passage in the territorial sea, including Articles 17-32.
- Article 17 establishes the right of innocent passage for ships of all States through the territorial sea.
- Articles 18-19 define passage and innocent passage; passage must not be prejudicial to the peace, good order, or security of the coastal State.
- Articles 21-22 permit coastal State laws and sea-lanes / traffic separation schemes in territorial seas.
- Article 24 constrains coastal States from hampering innocent passage except in accordance with UNCLOS.

## Source: IMO MASS search results
URLs found:
- https://www.imo.org/en/mediacentre/hottopics/pages/autonomous-shipping.aspx
- https://www.imo.org/en/mediacentre/meetingsummaries/pages/msc-110th-session.aspx

Key points for dataset design:

- The IMO is developing a Maritime Autonomous Surface Ships (MASS) Code.
- Search results indicate MSC 109 revised the roadmap, with finalization/adoption of the non-mandatory MASS Code expected at MSC 111 in May 2026. This updates earlier project assumptions that referenced non-mandatory adoption in 2025.
- Dataset scenarios should avoid claiming operational legality for autonomous decisions; they should test decision-support and exception handling with explicit authority boundaries and human escalation.

## Practical design implications

- Use tags that distinguish explicit COLREGs rules from maritime operational policy and generic ROE.
- Treat ROE as synthetic/generic policy text in the benchmark, not as an official military ROE source.
- Authority structures should specify who may approve delay, speed reduction, route deviation, restricted-water entry, post-incident reporting, and any action with political/military escalation risk.
- Gold escalation choices should be conservative where sensor uncertainty, collision risk, rule ambiguity, environmental hazard, or force-protection ambiguity exists.

## Exact rule excerpts used for tags

The converted COLREGs reference provides the exact rule text for selected tags. Rule 5 requires a proper lookout by sight, hearing, and all available means. Rule 6 requires safe speed so the vessel can take proper and effective collision-avoidance action and stop within an appropriate distance. Rule 7 requires all available means to determine collision risk, says that doubt means risk is deemed to exist, and warns against assumptions based on scanty information. Rule 8 requires positive, timely, and readily apparent action to avoid collision, with speed reduction or stopping if needed to avoid collision or allow more time to assess. Rule 14 requires reciprocal-course power-driven vessels with collision risk to alter to starboard and, when in doubt, assume a head-on situation exists. Rule 15 requires the vessel with another power-driven vessel on her own starboard side to keep out of the way and avoid crossing ahead. Rule 17 requires the stand-on vessel to keep course and speed initially, but permits and then requires action if the give-way vessel is not acting appropriately or collision cannot otherwise be avoided.

The UNCLOS reference establishes the innocent-passage tags. Article 17 gives ships of all states the right of innocent passage through the territorial sea. Article 18 says passage must be continuous and expeditious, with stopping or anchoring permitted when incidental to ordinary navigation, force majeure, distress, or rendering assistance. Article 19 defines passage as innocent so long as it is not prejudicial to the peace, good order, or security of the coastal state, and lists prejudicial acts such as weapons practice, intelligence collection, survey activity, serious pollution, fishing, and activities not directly bearing on passage. Article 21 permits coastal-state laws for safety of navigation, maritime traffic, environmental protection, and related matters, and requires foreign ships exercising innocent passage to comply with such laws and generally accepted collision-prevention regulations. Article 22 permits coastal states to require the use of designated sea lanes or traffic separation schemes where necessary for navigational safety. Article 24 says coastal states shall not hamper innocent passage except in accordance with UNCLOS.
