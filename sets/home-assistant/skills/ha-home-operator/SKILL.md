---
name: ha-home-operator
description: Use for a one-off Home Assistant device-control request or a question about current device/sensor state. Do not use for scheduled routines, system repair, or configuration work.
---

# HA home operator

Answer current-state questions and carry out clearly requested one-off device operations within the user's verified permissions.

Read [the HA tool safety contract](references/ha-mcp-safety.md). If the private setup profile is missing or stale in a way that affects authority or targeting, hand off to `ha-setup-and-conventions`.

## Workflow

1. Classify the request as a read-only status question or a state-changing action. A request for a repeated/scheduled behavior belongs to `ha-automation-workbench`.
2. Resolve the exact entity/device/area and action from current, narrow context. In this workspace, `GetLiveContext` is the first choice for current state and registered Assist intent/domain tools are the ordinary control surface. Use HA-MCP control only when the exact tool is discovered with `ha_search_tools`, its full schema is inspected, and identity, permissions, and allowlist are verified.
3. For a read, query only the relevant entity/domain/area and report its current state and freshness. Do not infer historical behavior from a current-state result.
4. For a write, state the exact target, requested end state, and effect. Resolve ambiguous names and groups before asking for fresh confirmation. Treat custom scripts as opaque until their documented scope and side effects are understood.
5. After confirmation, call only the approved tool once. Read back the relevant state to verify the outcome. If state is unavailable or unchanged, report that the result is unverified and stop.

## Special handling

- Resolve the intended lock state explicitly. Some Assist intent descriptions map turn-on to lock and turn-off to unlock; never paraphrase a lock request as vague on/off.
- Treat covers, doors, gates, water/gas controls, climate, vacuums, broadcasts, and scripts as consequential operations. Explain effect and target before confirmation.
- If a needed control tool is unavailable, denied, or broader than the request, stop and explain the manual path. Do not switch to an administrator credential.

## Handoffs and non-goals

- Repeated routines or conditional behavior → `ha-automation-workbench`.
- Unexpected/unexplained behavior → `ha-failure-triage`.
- Installation/configuration changes → `ha-config-integrations`, `ha-system-maintenance`, or `ha-esphome-device-maintenance` as applicable.
- This skill does not create automations, change permissions, perform system maintenance, or infer a household member's consent.

## Completion check

For a read, the answer names the relevant observation and any freshness/availability limit. For a write, the exact action was confirmed, the result was read back, and any uncertainty is explicit. No unrelated entities or state were queried.
