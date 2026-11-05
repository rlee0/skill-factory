# Home Assistant agent skill set

**Status:** Draft; tool behavior is untested and release-blocked pending an isolated, non-production HA/MCP evaluation and authorized review.

This set is designed for one owner/operator managing a Home Assistant home through Assist, HA-MCP, and, where separately available, ESPHome Device Builder. It is portable by intent. Evaluation target: OpenCode v2.2.5 with `opencode-go/gpt-6-luna`; no behavioral compatibility has been tested.

## Members

| Skill | Responsibility |
|---|---|
| [`ha-setup-and-conventions`](ha-setup-and-conventions/SKILL.md) | Establish a minimal, private, user-approved setup and conventions profile. |
| [`ha-home-operator`](ha-home-operator/SKILL.md) | Handle one-off device control and current-state questions. |
| [`ha-failure-triage`](ha-failure-triage/SKILL.md) | Diagnose unexpected behavior from available read-only evidence. |
| [`ha-automation-workbench`](ha-automation-workbench/SKILL.md) | Design, review, and carefully edit automations and scripts. |
| [`ha-system-maintenance`](ha-system-maintenance/SKILL.md) | Plan and, when verified, perform backups, updates, and recovery. |
| [`ha-config-integrations`](ha-config-integrations/SKILL.md) | Work on non-automation HA configuration and integrations. |
| [`ha-esphome-device-maintenance`](ha-esphome-device-maintenance/SKILL.md) | Maintain ESPHome device configuration and firmware workflows. |
| [`ha-energy-comfort-advisor`](ha-energy-comfort-advisor/SKILL.md) | Give evidence-bounded energy and comfort advice. |

Each member bundles its own `references/ha-mcp-safety.md` so it remains usable when distributed independently. Keep those copies aligned when updating safeguards. A user-provided, already-mounted Samba path is a read-only source for HA config and automation YAML only; there is no SMB connector, mount operation, or share-write support. Keep the user's home profile and mount path outside this portable skill package. Do not put credentials, private routines, entity names, or household-specific custom tool names in these files.

## Review gates

- The user approved the domain brief, opportunity map, eight-member architecture, and an integration plan for draft authoring.
- Read-only Samba path support for HA configuration and automation YAML is approved as a local filesystem input, not as an MCP capability. The share path is not yet provided or verified as accessible to OpenCode.
- `opencode.jsonc` registers `./skills` for OpenCode discovery. This changes skill discovery only; it does not alter the configured MCP server or its permissions.
- The active MCP tool catalog is session-specific. The skills discover exact tools and schemas at use time and must not infer authorization from registration.
- No live HA tools were called during authoring. The current tool catalog is session-specific; dynamic tool availability and authorization must be checked at runtime.
- Evaluation cases are included, but no behavioral evaluation has run. Tool behavior needs synthetic data and test-only credentials in an isolated HA/MCP environment.
- **License:** Apache-2.0 under the parent repository's default license.
- The parent repository has a structural checker. The `skills-ref` reference validator was unavailable during registration, so its additional format validation remains outstanding.
