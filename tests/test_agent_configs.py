"""Check project subagent files against the Cursor frontmatter fields."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".cursor" / "agents"
ALLOWED_KEYS = {"name", "description", "model", "readonly", "is_background"}
EXPECTED = {
    "cv": "cv",
    "fullstack": "fullstack",
    "qa": "qa",
}


def _frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    end = text.find("\n---\n", 4)
    assert end != -1, path
    body = text[end + 5 :].strip()
    assert body, f"{path} has an empty prompt"
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def test_three_flat_subagents_have_supported_frontmatter() -> None:
    files = sorted(AGENTS.glob("*.md"))
    assert [path.stem for path in files] == ["cv", "fullstack", "qa"]
    for path in files:
        meta = _frontmatter(path)
        assert set(meta) <= ALLOWED_KEYS
        assert meta["name"] == EXPECTED[path.stem]
        assert len(meta["description"]) > 40
        assert meta["model"] == "inherit"
        assert meta["readonly"] == "false"
        assert meta["is_background"] == "false"


def test_boss_instructions_exist_and_there_is_no_nested_agent_tree() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Boss" in agents
    assert not (AGENTS / "boss.md").exists()
    assert not list(AGENTS.rglob("*/agents/*.md"))
