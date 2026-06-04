---
name: pickup
description: Resume a shelved work chain — surface the recorded git state and pickup hints from a prior /forge:handoff. Use for /forge:pickup, /forge:pickup <slug>, "pick up where I left off", "resume the work on X".
---

# Pickup

Resume work shelved by `/forge:handoff` — locate the shelved session note (or local forge handoff file), surface its `## Pickup hints` and recorded git state, and flip the note back to active.

> Full resume orchestration (lore finder, symmetric degraded read, no-rebase announcement) is built in a following slice. This skill is registered from the start so the dev-ritual pair `/forge:handoff` + `/forge:pickup` is a stable contract.
