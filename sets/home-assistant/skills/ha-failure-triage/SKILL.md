---
name: ha-failure-triage
description: Use when a Home Assistant device, integration, automation, or system component is failing or behaving unexpectedly. Diagnose from read-only evidence and propose a bounded next step; do not perform repairs.
---

# HA failure triage

Produce an evidence-backed explanation of an unexpected Home Assistant behavior, with uncertainty and a clear handoff for any change.

Read [the HA tool safety contract](references/ha-mcp-safety.md). If authority, installation facts, or relevant conventions are missing, consult `ha-setup-and-conventions` rather than assuming.

## Workflow

1. Ask for the symptom and approximate time/window if not provided. Identify the affected device, integration, automation, or user-visible outcome without requesting unnecessary private details.
2. Build a minimal evidence plan. In this workspace, start with a narrow `ha_get_overview`, `ha_search`, or `GetLiveContext` read as appropriate. Discover history, logs, traces, repairs, or integration-health operations with `ha_search_tools`; use them only if the exact tool is enabled and authorized in this deployment. If the user supplies an exact mounted-share YAML path, it may be read as separate config evidence under the shared Samba boundary and the exact OpenCode read permission.
3. Inspect warnings and pagination/partial-result fields. Fetch full configuration or a narrower time range when needed. A missing row in partial data is not proof that an event did not occur.
4. Separate observations from hypotheses. Distinguish file-backed configuration from live HA state; report divergence rather than assuming either source is current. Correlate timestamps, conditions, unavailable entities, and relevant changes only when the sources support it. Give confidence and list evidence that could change the conclusion.
5. Return likely causes in ranked prose, the supporting evidence, missing data, and the safest next diagnostic step. If needed evidence is not available through MCP, ask the user to provide a redacted log/trace excerpt or inspect the named HA UI page.
6. Hand off any proposed edit/restart/update to the matching skill. This skill remains read-only even if the apparent fix seems obvious.

## Handoffs and non-goals

- Automation/script correction → `ha-automation-workbench`.
- Configuration or integration changes → `ha-config-integrations`.
- Backup/update/restore → `ha-system-maintenance`.
- ESPHome firmware/config → `ha-esphome-device-maintenance`.
- This skill does not promise logs, history, traces, or health data are exposed in every deployment. It does not clear repairs, restart devices, run automations, or change configuration.

## Completion check

The response includes the symptom/time scope, the exact available evidence and its limitations, observations distinct from hypotheses, a confidence-qualified explanation, and either a safe next read or an explicit human/tool handoff. No write occurred.
