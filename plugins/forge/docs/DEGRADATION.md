# Degradation Reference

This document describes how forge skills degrade gracefully when optional extension points are not
configured. Every stripped capability announces itself with a visible-skip notice rather than
silently omitting a step.

## How to read this table

| Column | Meaning |
|--------|---------|
| **Capability** | The extension point or optional integration |
| **How it degrades** | What the skill does when the integration is absent |
| **How it surfaces to the user** | The visible-skip phrase or message emitted |
| **Re-add path** | How to configure the integration to restore full behavior |

## Degraded capabilities

| Capability | How it degrades | How it surfaces to the user | Re-add path |
|---|---|---|---|
| `feature_flags` — Feature flag provider (planning, step 7) | The flag-touchpoint mapping decision still happens (mandatory when the spec declares a flag), but provider-specific naming and the flag-configuration skill dispatch are skipped | "no feature-flag provider configured — see the extend guide" printed at the flag-touchpoint step | Configure a flag provider; add provider-specific naming conventions and a flag-configuration skill to your plugin |
| `observability` — Observability / alerting provider (planning skill, step 7b; planner agent, step 6b + spec template) | The Observability & Failure Visibility decision still happens (mandatory), but provider-specific metric naming, alert-rule generation, and health-check wiring are skipped | "no observability provider configured — see the extend guide" printed at the provider step | Configure an observability provider; add provider-specific metric conventions and an alert-configuration skill to your plugin |
| `issue_tracker` — Issue tracker / project management (planning, step 9) | The plan is written to the vault; no ticket is created or advanced | "no issue tracker configured — status sync skipped" printed at the ticket-advancement step | Configure an issue tracker; add a tracker-sync skill to your plugin and hook it into the plan-write step |
| `feature_flags` — Feature flag provider (subagent-driven-development, Pre-Loop) | The both-states (on/off) test-coverage discipline still applies when the plan declares a flag, but provider SDK detection, flag creation, and first-touch wire-up are skipped | "no feature-flag provider configured — flag setup skipped" printed at the Pre-Loop flag-setup step | Configure a flag provider; add a flag-configuration skill to your plugin and dispatch it at the Pre-Loop step |
| `issue_tracker` — Issue tracker / project management (subagent-driven-development, loop entry + after-all-slices) | Slices are dispatched and verified normally; the work item's status is never advanced (no "in progress" / "complete" transition) | "no issue tracker configured — status transitions skipped" printed at the loop-entry and after-all-slices status steps | Configure an issue tracker; add a tracker-sync skill to your plugin and hook it into the loop-entry and after-all-slices steps |

## Lighter-weight seams

These extension points are tagged in the shipped skills and agents but do not
produce a degradation banner, because the "default" behavior is simply the
generic path with no provider assumed:

| Extension point | Where it is tagged | Behavior without configuration | How you fill it |
|---|---|---|---|
| `build_test_commands` — the build/test/lint command the `test-runner` agent runs | `test-runner` agent frontmatter | The agent is stack-agnostic by design — it runs whatever command the caller supplies per invocation. There is no default command and no visible-skip banner; the caller always provides the command. | Pass your project's test runner, lint tool, or CI script as the command when you dispatch `test-runner`, or write a thin app skill that always supplies your stack's commands. |

## Cross-plugin seams (lore-side)

The following extension point is tagged in **lore**'s skills, not forge's. It
is listed here so the full set of extension points is discoverable from one
place, but the canonical reference and re-add path live in **lore**:

| Extension point | Owned by | Reference |
|---|---|---|
| `design_mockup` — UI mockup generation in the `brainstorm` skill | lore (`plugins/lore/skills/brainstorm`) | See lore's `plugins/lore/docs/DEGRADATION.md` for the visible-skip phrase and re-add path. |

## Removed, not degraded

Some capabilities present in the upstream private skill were **removed entirely** during
genericization — they have no extension point and no visible-skip notice, because they do not
exist in the generic skill at all:

| Capability | Status |
|---|---|
| Plan cost estimation (cost estimate step, session-totals hook, cost-history report) | Removed, not degraded — the generic planning skill has no cost-estimation step, no session-note cost hook, and no extension point for one. |
