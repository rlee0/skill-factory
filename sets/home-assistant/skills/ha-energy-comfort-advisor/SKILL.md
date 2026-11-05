---
name: ha-energy-comfort-advisor
description: Use when the user asks about Home Assistant energy use, historical sensor trends, or comfort schedules. Give evidence-bounded, read-only analysis and route any automation change to its dedicated skill.
---

# HA energy and comfort advisor

Explain configured energy/comfort data and offer options without changing device state, energy preferences, or automations.

Read [the HA tool safety contract](references/ha-mcp-safety.md). Use the user's approved privacy, units, and comfort preferences when present; ask if a material preference is missing.

## Workflow

1. Clarify the question, time window, relevant energy/comfort outcome, and whether the user wants a current reading or a trend. Do not infer billing rates, occupancy, or comfort preferences.
2. Discover an exact read tool for relevant energy, history/statistics, or sensor data with `ha_search_tools`; verify it is enabled and authorized. `GetLiveContext` provides current state, not a historical trend. Use a narrow time window and only the relevant sensors.
3. Check units, timestamps/timezone, gaps, resets, sensor meaning, and whether the data covers the requested window. Distinguish measured values from estimates. If required data is unavailable, say what is missing and offer a user-provided export/UI path.
4. Summarize observations with the source and timeframe. Explain uncertainty and avoid causal claims unless the data supports them. Label recommendations as options, including comfort trade-offs and assumptions.
5. Keep advice read-only. If the user wants a schedule or device change, hand off to `ha-automation-workbench` or `ha-home-operator`, where exact targeting and fresh confirmation apply.

## Handoffs and non-goals

- Unexpected sensor/device behavior → `ha-failure-triage`.
- Automation or device change → `ha-automation-workbench` or `ha-home-operator`.
- This skill does not change Energy dashboard preferences, create schedules, control devices, promise savings, or substitute for a qualified energy audit.

## Completion check

The response answers the stated question using available, relevant data; names units, timeframe, source, and gaps; separates observation from estimate/recommendation; and performs no write. If the requested trend cannot be supported, it says so rather than inventing one.
