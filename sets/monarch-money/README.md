# Monarch Money

**Purpose:** provide careful, user-directed help reviewing and organizing Monarch Money records, including finance check-ins, budget scenarios, category setup, transaction cleanup, merchant normalization, goals, and debt/cash-flow comparisons.

**Version:** `0.1.0` (draft; behavioral evaluation pending)

**License:** Apache-2.0 (repository default)

**Runtime status:** OpenCode is the target runtime; no runtime has passing behavioral evidence for this set.

## Members

| Skill | Use it when |
| --- | --- |
| [`monarch-finance-manager`](skills/monarch-finance-manager/SKILL.md) | Routing a broad Monarch or personal-finance request to a focused skill. |
| [`monarch-finance-check-in`](skills/monarch-finance-check-in/SKILL.md) | Preparing an evidence-bounded overview of connected finance records. |
| [`monarch-budget-planning`](skills/monarch-budget-planning/SKILL.md) | Reviewing budgets and building user-priority-led target scenarios. |
| [`monarch-category-setup`](skills/monarch-category-setup/SKILL.md) | Reviewing category meanings or proposing taxonomy changes. |
| [`monarch-transaction-cleanup`](skills/monarch-transaction-cleanup/SKILL.md) | Reviewing transactions, categories, tags, splits, or requested rules. |
| [`monarch-merchant-normalization`](skills/monarch-merchant-normalization/SKILL.md) | Auditing possible merchant aliases or duplicates. |
| [`monarch-goal-maintenance`](skills/monarch-goal-maintenance/SKILL.md) | Reviewing or changing savings goals and tracking allocations. |
| [`monarch-debt-cash-scenarios`](skills/monarch-debt-cash-scenarios/SKILL.md) | Comparing illustrative debt-payoff or cash-flow scenarios. |

## Data, evaluation, and safety

The source glossary contains only general terminology; it is not a household-specific category inventory. It does not include a connected household's settings, transactions, balances, or account identifiers. Use a user's approved private glossary when supplied, and keep that private glossary outside this set and its consumer archive.

Evaluation cases are fixtures, not results. No behavioral evaluation has run, and no runtime is tested. The skills are not financial, tax, investment, credit, legal, or other professional advice. Keep all writes separately authorized and do not release this draft until evaluation and risk-based safety review are complete.

See the [general terminology](GLOSSARY.md), [research notes](docs/research/), and [evaluation protocol](../../docs/evaluation.md).
