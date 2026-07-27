"""Contract tests for the deploy-oo-chat skill."""

from pathlib import Path

import yaml


SKILL_PATH = (
    Path(__file__).parents[1]
    / ".claude"
    / "skills"
    / "deploy-oo-chat"
    / "SKILL.md"
)


def _skill_parts():
    content = SKILL_PATH.read_text(encoding="utf-8")
    _, yaml_text, body = content.split("---", 2)
    return yaml.safe_load(yaml_text), body


def test_uses_connectonion_tools_frontmatter():
    frontmatter, _ = _skill_parts()

    assert frontmatter["name"] == "deploy-oo-chat"
    assert "allowed-tools" not in frontmatter
    assert "Bash(git *)" in frontmatter["tools"]
    assert {"read", "edit"} <= set(frontmatter["tools"])


def test_documents_claude_and_co_ai_invocation():
    _, body = _skill_parts()

    assert "/connectonion:deploy-oo-chat" in body
    assert 'co ai --yolo "/deploy-oo-chat"' in body
    assert "--yolo-turns" in body


def test_dry_run_stops_before_mutating_steps():
    _, body = _skill_parts()
    safety = body.index("## Safety contract")
    steps = body.index("## Steps")
    dry_run_stop = body.index("For `--dry-run`, stop here.")

    assert safety < steps < dry_run_stop
    assert "Do not edit files" in body[safety:steps]
    assert "Automated validation and forward tests must use `--dry-run`." in body


def test_release_steps_keep_manifests_and_original_dependency_consistent():
    _, body = _skill_parts()

    assert "git ls-remote origin refs/heads/main" in body
    assert "npm version {NEW_VERSION} --no-git-tag-version --ignore-scripts" in body
    assert 'npm install "connectonion@^{NEW_VERSION}"' in body
    assert "If and only if the preflight dependency started with `file:`" in body
