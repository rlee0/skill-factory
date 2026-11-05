---
name: ha-automation-workbench
description: Use when the user wants to design, explain, debug, create, or modify a Home Assistant automation or script. Keep proposed edits separate from execution and require fresh confirmation for each write or run.
---

# HA automation workbench

Help the user create and maintain automations/scripts with an explicit preview, best-practice checks, and controlled application.

Read [the HA tool safety contract](references/ha-mcp-safety.md). Before designing or editing, load the tool-required HA best-practices guide or the exact current local reference it names. If required guidance is unavailable, stop before writing. If the user's conventions profile is missing or stale, ask setup to establish them.

## Workflow

1. Clarify desired trigger, conditions, actions, target, timing, exceptions, and expected behavior. Distinguish a one-off control request (home operator) from a repeated routine.
2. In this workspace, use `ha_config_get_automation` to read the existing configuration and hash, `ha_get_skill_guide` or the exact local reference it names for current best practices, and `ha_config_set_automation` only after inspecting its full schema. If those tools are absent, discover exact alternatives with `ha_search_tools`. Record the current precondition and affected entities. Consult current Home Assistant guidance for syntax and platform version.
   - If the user supplies a mounted-share path to automation YAML, read only the named file under the shared Samba boundary and exact OpenCode read permission. Treat it as separate from the live automation returned by MCP; check for divergence before recommending an edit.
3. Draft a minimal configuration or diff. Explain when it runs, which conditions gate it, affected targets, failure behavior, and any physical or privacy impact. Prefer native triggers/conditions/actions over templates when appropriate.
4. Validate the draft using available documentation or validation tools. Do not run actions to test a draft. If static validation or preview is unavailable, state that limitation.
5. Before applying, show the exact diff/target and consequence and request fresh confirmation for this write. Use a current hash/precondition when supported. If the precondition changed, reread and redraft; never overwrite unseen edits. Never write the Samba file; if it is the source of truth and cannot be safely changed through the matching HA-MCP operation, return a diff for the user to apply.
6. Treat enabling/disabling, manually running actions, and taking control of a blueprint as separate operations requiring their own explanation and confirmation. A manual action run can skip normal triggers and conditions; blueprint takeover may be one-way.
7. After an approved write, reread the automation and verify the stored configuration. Do not claim runtime behavior was tested unless it was tested in a suitable isolated environment.

## Tool-specific boundary

Prefer dedicated structured automation operations. Avoid expression-transform modes unless the owner has separately reviewed the exact behavior and a safe evaluation path; a constrained expression interface is not a security sandbox. Use generic tool dispatch only for an exact, discovered, allowlisted tool.

## Handoffs and non-goals

- Current-state/device control → `ha-home-operator`.
- Evidence collection for a failure → `ha-failure-triage`.
- Non-automation YAML/integration/resource work → `ha-config-integrations`.
- ESPHome device automations → `ha-esphome-device-maintenance`.
- This skill does not silently enable, run, delete, or convert automations, and does not edit upstream Home Assistant code.

## Completion check

The user has a reviewable draft/diff with behavior and effects explained; validation limits are explicit; each write or run has separate fresh confirmation; and the stored result is verified or clearly reported as unverified. No draft is described as runtime-tested without isolated evaluation evidence.
