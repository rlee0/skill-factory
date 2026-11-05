---
name: ha-system-maintenance
description: Use when the user asks for Home Assistant health review, backup, update, restore, or recovery planning. Verify installation support and require fresh confirmation for every maintenance operation.
---

# HA system maintenance

Plan and, when the connected installation exposes a verified tool, assist with maintenance and recovery while preserving a known recovery path.

Read [the HA tool safety contract](references/ha-mcp-safety.md). Check the current private setup profile and verify the active installation type, Supervisor availability, MCP tool schema, and permissions before recommending an operation.

## Workflow

1. Clarify the maintenance goal, urgency, affected services, acceptable interruption, and recovery expectations. Do not infer a maintenance window or user tolerance.
2. Perform a narrow read-only preflight: current relevant version/health/repairs, supported backup/update operations, existing backup status if available, and known incompatibilities. Mark missing data and installation-dependent features.
3. Present a staged plan: prerequisites, proposed operation, impact/downtime, backup/recovery path, verification, and a stop/rollback condition. Do not promise a restore will succeed.
4. Discover backup/update/restore operations with `ha_search_tools`, then inspect each full schema and effective availability. `ha_get_overview` metadata or a public HA-MCP tool list is not proof an operation is enabled. If no exact enabled tool exists, provide user-guided HA UI instructions and stop before execution. Do not route through `ha_call_tool` to find a broader credential or bypass a denial.
5. Obtain fresh confirmation for each backup, update, restore, restart, or other state-changing step. A backup does not authorize an update; an update does not authorize a restore.
6. Execute only one approved step at a time. Monitor the documented job/status source when available. If it times out or returns partial failure, inspect state before any retry; stop if the result is uncertain.
7. Verify service health and the intended result using narrow reads. Report what changed, what remains unresolved, and any manual recovery step.

## Handoffs and non-goals

- Unexpected component behavior → `ha-failure-triage`.
- Automation edits → `ha-automation-workbench`.
- General HA resource/integration changes → `ha-config-integrations`.
- ESPHome firmware or device configuration → `ha-esphome-device-maintenance`.
- This skill does not run unattended upgrades, infer installation support from public docs alone, or claim an operation is reversible without evidence.

## Completion check

The user has a staged plan with verified prerequisites and an explicit recovery limit. Every executed step had fresh confirmation, its status was checked, and unverified outcomes are reported as such. If a required tool or backup path is unavailable, the result is a manual handoff—not a claimed success.
