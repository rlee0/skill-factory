# Home Assistant

**Purpose:** provide cautious help with Home Assistant setup, device use, troubleshooting, automations, configuration, ESPHome, maintenance, and energy or comfort questions.

**Version:** `0.1.0` (draft; behavioral evaluation pending)

**License:** Apache-2.0 (repository default)

**Runtime status:** OpenCode is the target runtime; no runtime has passing behavioral evidence for this set.

## Members

| Skill | Use it when |
| --- | --- |
| [`ha-setup-and-conventions`](skills/ha-setup-and-conventions/SKILL.md) | Onboarding or refreshing a private, user-approved Home Assistant conventions profile. |
| [`ha-home-operator`](skills/ha-home-operator/SKILL.md) | One-off device control or current-state questions. |
| [`ha-failure-triage`](skills/ha-failure-triage/SKILL.md) | Diagnosing unexpected device, integration, automation, or system behavior. |
| [`ha-automation-workbench`](skills/ha-automation-workbench/SKILL.md) | Designing, reviewing, or carefully changing automations and scripts. |
| [`ha-system-maintenance`](skills/ha-system-maintenance/SKILL.md) | Planning health checks, backups, updates, restores, or recovery. |
| [`ha-config-integrations`](skills/ha-config-integrations/SKILL.md) | Non-automation Home Assistant configuration and integration work. |
| [`ha-esphome-device-maintenance`](skills/ha-esphome-device-maintenance/SKILL.md) | ESPHome configuration, validation, compilation, and device maintenance. |
| [`ha-energy-comfort-advisor`](skills/ha-energy-comfort-advisor/SKILL.md) | Evidence-bounded analysis of energy use, sensor trends, and comfort schedules. |

## Evaluation and safety status

Evaluation cases are fixtures, not results. No behavioral evaluation has run, and tool behavior has not been tested in an isolated Home Assistant/MCP environment. Do not treat this draft as approved for live or consequential use. Any deployment needs exact runtime/tool checks, a risk-based safety review, and qualified review before consequential use.

The skills default to read-only investigation, fresh confirmation for every write or side effect, and keeping household profiles and mount paths outside this portable set. The shared safety contract is copied into each member's `references/` directory so each skill can be packaged independently.

See the [domain brief](GLOSSARY.md) and [evaluation protocol](../../docs/evaluation.md).
