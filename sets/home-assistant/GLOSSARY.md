# Domain brief: Home Assistant home management and maintenance agent

**Status:** Approved for the updated scope, including read-only access to a user-mounted Samba path for HA configuration and automation YAML. This brief is for skill-set discovery, not authorization to operate a Home Assistant installation.

## Purpose and intended users

Design a reusable suite of agent skills to help the user manage and maintain their own Home Assistant-powered home through an HA MCP connection. The primary user is the homeowner/operator. Other residents, guests, and people affected by devices or automations may be impacted, but are not currently intended skill users.

## People affected

- The user, who reviews diagnoses and approves changes.
- Other household residents and guests, who may be affected by device control, automations, access, privacy, comfort, or safety.
- People whose presence or activity is represented by sensors or home records; their details should not be copied into reusable skill files.

## Recurring workflows

The user selected all of these areas for inclusion; relative priority is not yet established:

- Troubleshoot device, integration, and system failures.
- Design, review, and modify automations/scripts.
- Perform system health checks, backups, updates, and recovery.
- Maintain YAML and ESPHome configurations and related device workflows.
- Control devices and answer everyday home questions.
- Review energy use and suggest comfort or efficiency improvements.
- Onboard the agent to the current HA/MCP setup and align on user-approved standards and conventions for the other skills to follow.

The user wants deep technical coverage, including integrations, YAML, ESPHome, updates, and recovery. Exact current procedures, handoffs, and a representative task have not yet been provided.

The user selected an onboarding/conventions capability: it should gather setup facts read-only, align standards with the user, and maintain a private, approved home profile for other skills. It should not make HA configuration changes as part of onboarding.

The user also wants the configuration and automation skills to read HA configuration/YAML from a Samba share that the user has already mounted and can provide by path. Start read-only. Do not mount the share, handle SMB credentials, or write through the share. The actual path and its visibility to OpenCode are not yet verified.

## Desired outcomes and success signals

**User-provided:** The suite should support the workflow areas above, be reusable across different Home Assistant/MCP deployments while adapting to the user's setup, require the user's fresh confirmation before every write, and include a setup/onboarding workflow that aligns conventions for use by other skills.

**Provisional hypotheses to review:** Useful outcomes may include faster evidence-backed diagnosis, changes that are understandable and reviewable before application, successful recovery from maintenance issues, and convenient everyday help without surprising residents. No concrete success measure or example task has been supplied yet.

## Constraints and boundaries

- Read and diagnose without changing state; explain intended target and consequence and obtain fresh, specific user confirmation before every write. Do not infer standing consent from earlier approvals.
- No additional action categories were excluded, but all writes remain subject to the confirmation rule. High-impact actions (for example, operating locks, deleting configuration, changing secrets, restoring backups, updating systems, or flashing firmware) need especially clear target and consequence descriptions.
- Preserve the permissions and identity of the connected Home Assistant user. Do not treat MCP tool availability as proof that an action is authorized for every household user.
- Adapt to each installation's supported features, enabled MCP tools, permissions, and runtime. Exact installation type, Home Assistant version, MCP server/tool versions, and runtime are unresolved and should be verified during deployment adaptation rather than assumed.
- Onboarding may inspect only the minimum HA/MCP facts needed, read-only. It should make no HA changes. Other skills should use the current, user-approved home profile; if it is missing, stale, or conflicts with the request, ask rather than silently infer.
- Keep the deployment-specific profile separate from portable skill files and outside packaged skill archives by default. Its storage location and exact contents are unresolved; never store credentials or secrets in it.
- For Samba-backed inspection, use only the exact user-provided mount root and only for HA configuration and automation YAML. Verify that the path is mounted and readable inside OpenCode before use. Do not mount SMB, ask for SMB credentials, scan recursively, follow paths outside the approved root, read `secrets.yaml` or `.storage`, or write through the share. If a file is the source of truth, prepare a diff for the user; apply a change through HA-MCP only after verifying that the MCP object is the same resource and the user confirms it.
- Keep personal home details, addresses, entity/device names, credentials, and household routines out of reusable skill files by default. Use generalized examples unless a specific detail is necessary and explicitly approved for inclusion.
- The skills should guide the user; they are not permission to access or operate the user's live home during this discovery phase.

## Terminology

- **HA:** Home Assistant.
- **HA MCP:** The Model Context Protocol server/tools through which an agent can interact with a Home Assistant deployment. Tool availability and authorization may vary by deployment.
- **Write:** Any agent-triggered action that changes Home Assistant state or configuration, including device service calls as well as administrative edits.
- **Fresh, specific confirmation:** Approval for the exact proposed action, target, and consequence; it does not authorize later or broader actions.
- **Reusable skill:** A skill intended to adapt to different HA/MCP versions and setups rather than embedding this home's private configuration.
- **Home profile:** A proposed private, user-approved record of deployment facts and operating conventions that other skills consult. It is not a credential store or part of the portable skill package.
- **Mounted Samba path:** A user-provided local path to an already mounted share. It is a read-only reference source, not an HA-MCP endpoint or authorization grant.

## Representative edge cases

- MCP search or overview results may be partial, paginated, stale, or ambiguous; verify the exact entity/configuration before advising or acting.
- A device may be offline or a change may not produce the expected physical result; distinguish execution success from verified outcome.
- Automation actions run manually may bypass their normal triggers or conditions; explain this difference before any manual run.
- HA installation types differ in availability of Supervisor, backup, and update operations.
- Lock/security, climate, power, firmware, secrets, deletion, and restore actions can have consequences beyond an ordinary configuration edit.
- Other residents' preferences, privacy, and presence may affect whether a technically valid automation is appropriate.
- A home profile can become stale after an installation, tool, or preference change; skills must check its applicability and surface conflicts.
- A Samba file may differ from the live HA configuration or may be an incomplete backup. Treat it as a separate source and report divergence; do not assume it is active configuration.

## Preliminary risks and safeguards

- **Physical safety/security:** Require exact target and effect, explicit confirmation, and post-action verification for consequential device actions; stop on ambiguity.
- **Availability/data loss:** Explain blast radius and recovery path before configuration changes, updates, deletes, restores, or firmware operations; recommend backups when supported and appropriate.
- **Authorization:** Do not bypass HA permissions or use a broader shared credential to act for a less-privileged user. Deployment identity propagation and audit behavior require verification.
- **Privacy:** Minimize reads, avoid exposing household activity unnecessarily, keep deployment-specific profile data private, and exclude credentials and identifiable home data from packaged artifacts.
- **Incorrect diagnosis:** Cite the state/log/trace/config evidence used, flag missing or partial evidence, and distinguish hypotheses from confirmed causes.
- These are preliminary design safeguards, not a completed tool safety review or runtime evaluation.

## Evidence and provenance

- **User-provided:** The user wants a reusable suite for managing and maintaining their own home; selected deep technical coverage, all six operational workflow areas plus setup/conventions onboarding, adaptation across HA/MCP deployments, and confirmation before each write. The onboarding capability should gather read-only setup facts and maintain a private, approved profile for other skills. No concrete operational task example, deployment details, or quantified success criteria were provided.
- **User-provided:** The user wants a pre-mounted Samba path as an additional read-only source for Home Assistant configuration and automation YAML. The skills must not mount the share or write through it.
- **Sourced:** The research note [`docs/research/home-assistant-agent-capabilities-by-role.md`](docs/research/home-assistant-agent-capabilities-by-role.md), dated 2026-11-05, summarizes first-party Home Assistant documentation and the HA MCP tool definitions available in that session. It documents the distinction between ordinary entity control and admin/system-management capabilities, plus tool-specific caveats around partial searches, automation changes, and high-impact ESPHome operations. Its MCP catalog observations are session-specific, not a universal contract.
- **Sourced:** [`docs/research/home-assistant-mcp-session-capability-contract.md`](docs/research/home-assistant-mcp-session-capability-contract.md), dated 2026-11-05, compares official Home Assistant Assist/MCP documentation, the separate unofficial HA-MCP project docs/source, ESPHome Device Builder docs/source, and this session's tool metadata. It reports that several capabilities absent from the directly registered HA-MCP tool slice are publicly documented behind HA-MCP's dynamic search/call facade; actual deployment exposure, permissions, and identity semantics remain unverified.
- **Sourced:** OpenCode v2.2.5 skill discovery supports a project `skills` source in `opencode.jsonc`, now set to `./skills`. OpenCode documents separate `external_directory` permissions for paths outside the project; no Samba path permission has been configured because the mount path is not yet provided. [OpenCode skills](https://opencode.ai/docs/skills/); [OpenCode permissions](https://opencode.ai/docs/permissions/#external-directories).
- **Sourced, current tool-catalog snapshot (2026-11-05):** The registered tools available in this session total 103: 74 Assist tools (including 51 home-specific script shortcuts), 21 ESPHome device-builder tools, and 8 HA MCP server tools. The descriptions show direct entity control/context, overview/search, automation get/set/guidance, and ESPHome config/validation/compile/install/secret operations. This catalog does not expose direct history/log/trace, energy, backup/restore, or update-execution tools; generic tool search/call means that is not proof the underlying deployment can never expose them. Home-specific tool names are intentionally omitted from this reusable brief.
- **Sourced:** The HA-MCP source comparison in [`docs/research/home-assistant-mcp-session-capability-contract.md`](docs/research/home-assistant-mcp-session-capability-contract.md) says the current catalog exposes no direct SMB connector. Public HA-MCP File & YAML tools are opt-in and operate on paths available to the HA server, not as an SMB client. This does not prove the user's mounted share is accessible to OpenCode.
- **Assumptions:** “My home” means one household the user manages; the user is willing to consider any action class if each write receives fresh, specific confirmation; the suite should be portable but adapted before use. Confirm or correct these assumptions during review.
- **Unresolved:** Representative task and success signal; the user's permissions/role; installation type and version; whether this session's catalog matches the target deployment; generic dispatcher reach; credential, identity-propagation, audit, and allowlist semantics; available history/log/backup/update capabilities; whether the mounted path is readable within OpenCode and which files it contains; whether those files are the active configuration source; which standards/conventions the profile should collect; the profile's storage/update/review process; household-specific policies and preferences.

## Sensitive context to exclude from packaged skills

Do not include the user's address, account or credential data, identifiable household members, device/entity names, detailed occupancy patterns, or private routines. Keep deployment-specific standards/profile data out of reusable skills and packaged archives by default. Keep discovery-specific examples in this review conversation or a private, user-approved artifact.

## Decisions requiring expert or user review

- User approval or correction of this reopened brief's scope and assumptions before opportunity mapping.
- A concrete representative task and meaningful success signal, if the user wants the opportunity map grounded in a particular pain point.
- User review of which standards the onboarding workflow should capture and how the private profile will be stored and kept current.
- User approval of this Samba path boundary before the configuration and automation skills consume a real mount path.
- Deployment-specific identity, permission, tool-availability, and audit checks before recommending any live MCP integration behavior.
- Risk-scaled safety review and appropriate qualified review before any consequential tool-enabled skill is treated as safe for deployment.
