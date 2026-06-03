# forge

A portable **software-development** plugin for Claude Code: general-purpose dev
agents and dev-ritual skills that work in any project, with no app-specific
assumptions baked in.

forge is the dev-tooling sibling of [lore](../lore) (portable knowledge
management). Where lore owns *what you know*, forge owns *how you build*:
the reusable agents and rituals a developer reaches for regardless of which
codebase they're in.

## Status

**Skeleton (v0.1.0).** This repo currently ships only a proof-of-life agent
(`forge-ping`) that confirms plugin agent registration works. The 13 general
dev agents (`researcher`, `troubleshooter`, `code-reviewer`, `architect`,
`planner`, the `sdd-*` quartet, `doc-finder`, `test-runner`, `log-sifter`,
`pr-summarizer`, `code-simplifier`, …) are migrated here in a later phase.
Nothing app-specific belongs in forge; per-project automation stays in that
project's own repo.

## What lives here

- **Agents** (`plugins/forge/agents/`) — general dev subagents, dispatchable as
  `forge:<name>` once installed.
- **Skills** (`plugins/forge/skills/`) — dev-ritual skills (TDD loops, review
  cadences, …), invocable as `/forge:<name>`. *(none yet — populated later.)*

## Layout

```
.claude-plugin/marketplace.json   # local dev marketplace (source: ./plugins/forge)
plugins/forge/
  .claude-plugin/plugin.json      # plugin manifest
  agents/                         # dispatchable subagents
  skills/                         # /forge: ritual skills
tests/                            # packaging + registrability invariants
```

Claude Code rejects `source: "."` — the plugin must live in a `plugins/forge/`
subdir referenced by `source: "./plugins/forge"` in the root marketplace.

## Install (local dev)

```
/plugin marketplace add /path/to/forge
/plugin install forge@forge-local
```

Then restart the session and confirm with the `forge-ping` agent. See
[`MANUAL-SMOKE.md`](MANUAL-SMOKE.md) for the full boundary smoke test.

## Leak gate

A generic, denylist-driven pre-publish check that blocks a commit when a
private string would ship into a publishable repo. The mechanism ships **zero**
private strings — every forbidden token lives in a machine-local denylist that
is never tracked in any repo:

```
plugins/forge/scripts/leak_gate.py        # the gate (denylist-driven, fail-closed)
plugins/forge/scripts/install-hooks.sh    # chain-safe pre-commit installer
~/.claude/leak-gate.denylist              # machine-local denylist (UNTRACKED)
```

Run it directly:

```bash
python3 plugins/forge/scripts/leak_gate.py <tree> --denylist ~/.claude/leak-gate.denylist
# exit 0 clean · 1 leak (prints relpath:lineno:token) · 2 fail-closed
```

**Fail-closed:** a missing, unreadable, or pattern-empty denylist makes the gate
exit `2` (error) — it never exits `0` when it could not actually certify the
tree clean. The denylist format is one Python regex per line (`#` comments),
matched case-insensitively; use `\b` word-boundary anchors.

Install as a pre-commit hook. Pass every tree that ships publicly — the
shippable surface **and** `tests/` (test fixtures go public too) — but not
author-controlled root docs, which may legitimately carry the public repo-owner
URL:

```bash
plugins/forge/scripts/install-hooks.sh <repo> plugins/<name> tests
```

The installer is idempotent and chain-safe — an existing pre-commit hook is
preserved and run first. `.git/hooks/` is never committed, so the absolute paths
baked into the generated hook stay machine-local.

## Tests

```bash
python3 -m pytest -q
```

Covers manifest validity (`marketplace.json` / `plugin.json`) and agent
frontmatter registrability. The plugin-system boundary (actual install +
dispatch) is covered by `MANUAL-SMOKE.md`, which unit tests can't reach.
