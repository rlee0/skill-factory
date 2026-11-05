---
name: ha-setup-and-conventions
description: Use when onboarding a Home Assistant agent, when the HA/MCP deployment changes, or when its private conventions profile is missing or stale. Establish a minimal, user-approved setup and standards profile; do not configure Home Assistant.
---

# HA setup and conventions

Establish the current deployment context and the user's operating standards so the other HA skills can work consistently. The result is a private profile, not a permission grant.

Read [the HA tool safety contract](references/ha-mcp-safety.md) before inspecting tools or deployment metadata.

## Workflow

1. **Check existing context.** Ask for or read the user's private home profile if available. Note its last-verified date and which facts are user-confirmed, sourced, assumed, or unresolved. If it is current, use it instead of repeating onboarding.
2. **Inventory narrowly.** Inspect tool schemas/catalog metadata first. In this workspace, `ha_search_tools` discovers underlying HA-MCP tools and `ha_get_overview` can return scoped system metadata; inspect each schema before use. Distinguish Assist/Device control, official Core MCP, HA-MCP, and ESPHome Device Builder. If the user asks for deployment facts, use only the minimum metadata fields needed; explain before reading sensitive system/location data. Do not enumerate all entity states or configuration just to build the profile.
3. **Verify authority and capabilities.** Record only what can be verified about installation type/version, API surface, transport, effective tool allowlist, read-only mode, approval policy, logs, Supervisor support, YAML/file feature flags, and ESPHome access. A tool search result is not proof a tool is enabled. If authentication or identity behavior is unclear, mark it unresolved and ask the owner to verify it in the deployment settings.
   - A user-mounted Samba path is not an MCP tool. Record its root only if the user explicitly asks to keep it in the private profile; otherwise use a path supplied for the current task. Never attempt to mount it or capture SMB credentials. If OpenCode needs external-directory permission, scope it to that exact mount root and read-only access; do not broaden project permissions.
4. **Elicit standards.** Ask focused questions for user-approved conventions: naming/areas, automation style, maintenance and recovery preferences, privacy/data boundaries, action-confirmation expectations, and energy/comfort preferences if relevant. Do not ask for tokens, passwords, addresses, or unnecessary entity/device names.
5. **Draft the profile.** Separate verified setup facts from user-approved preferences. Add source and last-verified date to changing facts. Mark unknowns; do not invent defaults. Keep dynamic state (current device states, detailed history, occupancy) out of the profile unless the user explicitly approves a necessary, limited exception.
6. **Review and persist.** Show the whole proposed profile or a clear diff. Ask the user to approve the exact contents and destination before saving. Save only to a user-selected private location outside this portable skill package. If a private destination is unavailable, return the draft inline and mark it unpersisted.
7. **Hand off.** Tell the user which skills can use the profile. Any skill must recheck live state and permissions when acting; the profile never authorizes a tool call. If configuration changes are requested, hand off to the relevant skill and its fresh-confirmation flow.

## Profile shape

Use a compact structure; omit irrelevant fields and leave unknowns explicit:

```markdown
# Home profile
Status: draft / approved
Last reviewed: <date>

## Deployment facts
| Fact | Value | Source | Verified |

## Access and capabilities
| API/tool family | Verified availability and scope | Source | Verified |

## User-approved conventions
- Naming/areas:
- Automation style:
- Maintenance/recovery preferences:
- Privacy/data boundaries:
- Action confirmation:
- Energy/comfort preferences:

## Unresolved or stale
- <question, source needed, or recheck date>
```

The profile is user data, not skill-package content. Include only fields the user wants maintained; never put credential values or a broad entity list in it.

## Profile boundary

The profile may hold user-approved conventions and a dated capability summary. It is not a credential store, audit log, full entity inventory, or substitute for tool-schema discovery. Do not copy private tool/entity names into packaged skills. If another skill finds stale or conflicting profile content, stop and return here for review.

## Completion check

Onboarding is complete only when each recorded fact has a source/status and verification date, each convention is user-approved, unknowns remain visible, and the user has approved the exact private destination—or the draft is clearly marked as unpersisted. No HA configuration was changed.
