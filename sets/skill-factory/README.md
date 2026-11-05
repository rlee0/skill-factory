# Skill Factory

**Purpose:** help domain experts discover and map their work, design a tailored skill set, coordinate its approval-gated phases, author portable skills, evaluate behavior, review safety risks, and prepare a reviewed release.

## Members

| Skill | Use it when |
| --- | --- |
| [`author-skills`](skills/author-skills/SKILL.md) | Authoring or revising an independently usable Agent Skill from an approved design or bounded standalone request. |
| [`create-skill-set`](skills/create-skill-set/SKILL.md) | Coordinating the end-to-end factory workflow, decisions, approvals, and handoffs. |
| [`design-skill-set`](skills/design-skill-set/SKILL.md) | Designing tailored membership, responsibilities, handoffs, optional capabilities, and runtime assumptions from approved inputs. |
| [`discover-domain`](skills/discover-domain/SKILL.md) | Eliciting and reviewing the users, workflows, constraints, risks, and open questions behind a domain brief. |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | Clarifying shared domain language, testing conceptual boundaries, and recording significant domain decisions when useful. |
| [`integrate-tools-safely`](skills/integrate-tools-safely/SKILL.md) | Designing a justified tool/script integration with least privilege, safe failure behavior, and sandboxed evaluation gates. |
| [`maintain-skill-set`](skills/maintain-skill-set/SKILL.md) | Assessing post-release change impact, re-evaluation, independent versioning, runtime evidence, deprecation, or retirement. |
| [`research-domain`](skills/research-domain/SKILL.md) | Deepening a reviewed domain brief with focused, source-backed research when the domain warrants it. |
| [`evaluate-skills`](skills/evaluate-skills/SKILL.md) | Creating or reviewing behavioral evaluation cases and results. |
| [`map-skill-opportunities`](skills/map-skill-opportunities/SKILL.md) | Turning an approved domain brief into prioritized, bounded skill candidates. |
| [`release-skill-set`](skills/release-skill-set/SKILL.md) | Validating version, membership, license, evaluation, safety/sign-off, sandbox evidence, and archive before maintainer review. |
| [`runtime-adaptation`](skills/runtime-adaptation/SKILL.md) | Conditionally documenting named runtime differences and assessing runtime support evidence. |
| [`review-safety`](skills/review-safety/SKILL.md) | Reviewing skill and set risks before distribution, including required expert sign-off and release gates. |

**Version:** `0.3.0` (pre-release; behavioral evaluation passed for OpenCode)

**License:** Apache-2.0

**Runtime status:** OpenCode is the target and tested runtime for `0.3.0`; see the [versioned evaluation report](reports/0.3.0.json). The set is not yet released and awaits maintainer review of the exact report and archive; see the [safety review](../../docs/reviews/skill-factory-0.3.0-safety-review.md). The `0.1.0` report is a historical record for an earlier, incomplete fixture set and is not evidence for this version. See the repository [evaluation protocol](../../docs/evaluation.md).
