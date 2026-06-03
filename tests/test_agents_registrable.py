"""Every shipped agent must be registrable by Claude Code.

forge is agent-centric (its reason to exist is hosting general-dev agents). An
agent `.md` only registers as a dispatchable `subagent_type` if it opens with a
YAML frontmatter block carrying a non-empty `name:` and `description:`. This
test locks that invariant so an agent can't silently fail to register.

Live proof of the mechanism (KU1): the lore plugin's `lore-librarian` agent
appears in the running session's registry as the namespaced subagent_type
`lore:lore-librarian`. forge's agents register the same way as `forge:<name>`.
"""
from pathlib import Path

import pytest

AGENTS_DIR = Path(__file__).parent.parent / "plugins" / "forge" / "agents"


def _agent_files() -> list[Path]:
    return sorted(AGENTS_DIR.glob("*.md"))


def test_at_least_one_agent_ships():
    """forge's whole point is hosting agents — guard against an empty dir."""
    assert _agent_files(), "forge must ship at least one agent (the proof agent)"


@pytest.mark.parametrize("agent_md", _agent_files(), ids=lambda p: p.stem)
def test_agent_has_registrable_frontmatter(agent_md: Path):
    text = agent_md.read_text()
    assert text.startswith("---\n"), (
        f"{agent_md.name} must open with a `---` frontmatter block or Claude "
        "Code will not register it as a subagent_type"
    )
    end = text.find("\n---", 3)
    assert end > 0, f"{agent_md.name} frontmatter block is not closed"
    frontmatter = text[3:end]

    def _has(field: str) -> bool:
        return any(
            ln.strip().startswith(f"{field}:") and ln.split(":", 1)[1].strip()
            for ln in frontmatter.splitlines()
        )

    assert _has("name"), f"{agent_md.name} frontmatter must carry a non-empty `name:`"
    assert _has("description"), (
        f"{agent_md.name} frontmatter must carry a non-empty `description:` "
        "(it's what drives agent dispatch)"
    )
