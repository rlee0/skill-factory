---
name: ha-config-integrations
description: Use for non-automation Home Assistant configuration or integration work, such as helpers, scenes, dashboards, registries, or integration settings. Keep automation, ESPHome, and system update work in their dedicated skills.
---

# HA configuration and integrations

Help the user inspect and plan narrow Home Assistant configuration/integration changes. A public catalog entry is not proof the matching operation is enabled in this deployment.

Read [the HA tool safety contract](references/ha-mcp-safety.md). Check the private profile for naming and configuration conventions; verify current tool/schema, feature flags, and permissions before selecting an operation.

## Workflow

1. Clarify the desired configuration outcome, affected integration/resources, and current symptoms. Route automations/scripts to `ha-automation-workbench`, ESPHome devices to `ha-esphome-device-maintenance`, and backups/updates to `ha-system-maintenance`.
2. Use `ha_search` for narrow discovery where appropriate, then discover the exact resource-specific read tool with `ha_search_tools` and inspect its full schema. Read the relevant current resource; do not infer missing configuration from partial search results. If the user supplies a mounted-share path to YAML, read only the named file under the shared Samba boundary and exact OpenCode read permission, and treat it as a separate source from live HA configuration.
3. Prefer supported UI/resource-specific tools. If the requested action needs beta/opt-in File & YAML services, verify that feature is enabled and authorized before planning it. Avoid raw `.storage` edits and unreviewed file operations.
4. Prepare a minimal diff with source/version evidence, affected resources, expected effect, validation method, and recovery path. If the file is the source of truth, return a diff for the user to apply; do not write through Samba. If no validator or backup exists, say so.
5. Show the exact change and ask for fresh confirmation before each write. Use the tool's expected-value/hash precondition when available. If the resource changed, reread and prepare a new diff.
6. Apply only the confirmed change. Reread and validate the result. Do not broaden the operation to adjacent integrations or entities.
7. If no exact enabled tool or permission exists, stop and give a manual UI path. Never use generic tool dispatch as an authorization workaround.

## Handoffs and non-goals

- Automation/script work → `ha-automation-workbench`.
- Failure diagnosis → `ha-failure-triage`.
- Supervisor backup/update/restore → `ha-system-maintenance`.
- ESPHome YAML/device work → `ha-esphome-device-maintenance`.
- This skill does not edit Home Assistant Core source, change credentials/permissions, or assume file/YAML beta services are available.

## Completion check

The result contains a bounded diff or a clear manual handoff, exact tool and permission availability are established, validation/recovery limitations are explicit, and every applied write was freshly confirmed and verified.
