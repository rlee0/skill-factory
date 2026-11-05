---
name: monarch-finance-manager
description: Route broad requests to review or organize personal-finance records with the Monarch skill set. Use when the user wants help across multiple areas or is unsure where to start; focused requests belong to the relevant task skill.
---

# Monarch Finance Manager

Clarify broad personal-finance requests and direct the user to the focused skill that can handle them. This is a routing skill, not an autonomous financial manager.

## Workflow

1. Identify the requested outcome. If the request is broad or ambiguous, ask one concise question to distinguish review, planning, category setup, record cleanup, merchant cleanup, goal maintenance, or debt/cash scenarios.
2. Route to the focused skill:
   - category meanings, taxonomy, or category glossary → `monarch-category-setup`
   - overview, changes, recurring activity, account/net-worth, investment/credit, or goal status → `monarch-finance-check-in`
   - budget review or proposed category targets → `monarch-budget-planning`
   - transaction category, tag, split, or explicitly requested transaction-rule cleanup → `monarch-transaction-cleanup`
   - merchant name or duplicate normalization → `monarch-merchant-normalization`
   - creating/editing a goal or changing its tracking allocation → `monarch-goal-maintenance`
   - debt or cash-flow alternatives → `monarch-debt-cash-scenarios`
3. State the selected skill and the minimum information needed to continue. Do not claim automatic skill-to-skill invocation; ask the user to invoke the named skill if the runtime does not hand off.
4. For an out-of-scope request—payments, transfers, trades, tax work, recurring-schedule changes, or goal deletion—explain the boundary and offer a supported read-only alternative when useful.

## Authority and privacy

- Do not call Monarch tools, make a financial recommendation, or write records from this routing skill.
- Do not request account credentials or copy balances/transactions into skill resources.
- Category and merchant catalogs are household-level; mention that distinction when a request implies shared-record changes.

## Completion check

The request is classified, the correct skill and its boundary are named, and the user knows the next step. No financial data was read and no change was made.
