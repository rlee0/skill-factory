# 08: Evaluate activation and task outcomes

**What to build:** A maintainer can evaluate whether each skill activates appropriately and improves representative task outcomes against the target runtime's normal capabilities.

**Blocked by:** 04: Author portable skills from an approved design; 07: Review safety and obtain expert sign-off.

**Status:** ready-for-agent

- [ ] Create cases for relevant triggers, nearby irrelevant prompts, representative tasks, observable criteria, criticality, and repeat counts.
- [ ] Compare task outcomes with and without the candidate set against the same runtime baseline while retaining native runtime capabilities.
- [ ] Record exact runtime version, model identifier, loaded skill IDs, case results, and repeats for every tested runtime.
- [ ] Include every authored case in the evidence; do not infer support for untested runtimes or fabricate passing results.
- [ ] Block a passing release on any critical failure or serious safety regression; report non-critical failures transparently.
- [ ] Include cases that verify the evaluation capability itself handles missing evidence and unsupported runtimes honestly.
