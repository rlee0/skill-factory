---
name: ha-esphome-device-maintenance
description: Use for ESPHome device YAML, component, validation, compilation, firmware, or device-automation tasks. Treat device flashing and secrets as high-impact operations and keep them distinct from HA configuration.
---

# ESPHome device maintenance

Maintain ESPHome device configuration with a minimal read/compare/validate workflow. ESPHome Device Builder is a separate tool surface from Home Assistant Core and HA-MCP; verify its availability and authorization independently.

Read [the HA tool safety contract](references/ha-mcp-safety.md). Check the private profile for approved device conventions and the currently connected Device Builder surface.

## Workflow

1. Clarify the device goal and exact device/configuration. Discover the current tool schema and verify that the requested device and operation are in scope.
2. In this workspace, use the registered Device Builder list/read/docs tools (for example, `list_devices`, `get_config`, `get_component`, and `validate_config`) for the named device only. Never retrieve `secrets.yaml` values. Do not copy Wi-Fi credentials, tokens, or sensitive network details into the conversation or profile.
3. Draft the smallest change and explain affected components, pins, triggers, network/power behavior, and recovery implications where relevant. Use Device Builder's structured operations rather than hand-splicing YAML.
4. For an update, use the returned current content as the expected precondition; stop and reread if it changed. Validate the result, then compile when that is relevant and available. Explain that a queued compile/job is an external side effect and ask before starting it.
5. Treat device creation, component changes, automation edits, configuration replacement, deletion, compilation, firmware installation, and secret operations as distinct writes/jobs. Show exact target and effect and obtain fresh confirmation for each.
6. Firmware install requires a separate confirmation after configuration validation and successful compile. State that flashing can be irreversible, identify the precise device and transport, and explain offline/deferred behavior when the tool reports it. Do not install to real devices during evaluation.
7. Poll only the documented job ID/status. Verify the final device/job result; if interrupted, offline, or uncertain, stop and give a human recovery handoff.

## Secret handling

Never read secret values through the configuration getter. Secret replacement may be unrecoverable; prefer a manual user-managed secret update. If the user requests a secret operation, explain the consequence and keep it out of this automated workflow unless a separately reviewed, explicitly confirmed path is approved.

## Handoffs and non-goals

- HA integrations, helpers, or non-ESPHome YAML → `ha-config-integrations`.
- HA automation design → `ha-automation-workbench`.
- This skill does not assume a Home Assistant admin token authorizes Device Builder operations, and does not claim a compile or flash was safely tested without an isolated device sandbox.

## Completion check

The exact device and current config are identified; the minimal change is validated; each write/job has fresh confirmation; no secret value was read; and the final job/device status is verified or explicitly unresolved.
