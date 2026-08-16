import ast
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILLS = (
    "aaron-build-my-agent",
    "aaron-review-my-code",
    "linus-review-my-code",
)


def classify_project(source: str, has_host_yaml: bool = False) -> str:
    """Executable statement of the decision boundary documented by the skills."""
    tree = ast.parse(source)
    co_ai_import = any(
        isinstance(node, ast.ImportFrom)
        and node.module == "connectonion.cli.co_ai.agent"
        and any(name.name == "create_agent" for name in node.names)
        for node in ast.walk(tree)
    )
    hosts_agent = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "host"
        for node in ast.walk(tree)
    )
    if co_ai_import and hosts_agent:
        return "generated-co-ai"
    direct_sdk = any(
        isinstance(node, ast.Name) and node.id in {"Agent", "llm_do"}
        for node in ast.walk(tree)
    )
    if direct_sdk:
        return "direct-sdk"
    if has_host_yaml:
        return "generated-project"
    return "unclear"


class SingleTemplateContractTests(unittest.TestCase):
    def test_current_and_legacy_skill_copies_match(self):
        for name in SKILLS:
            current = ROOT / ".claude" / "skills" / name / "SKILL.md"
            legacy = ROOT / "commands" / f"{name}.md"
            self.assertEqual(current.read_bytes(), legacy.read_bytes(), name)

    def test_every_agent_skill_recognizes_both_project_shapes(self):
        for name in SKILLS:
            text = (
                ROOT / ".claude" / "skills" / name / "SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("create_agent", text, name)
            self.assertIn(".co/skills/", text, name)
            self.assertIn(".co/docs/", text, name)
            self.assertIn("direct sdk", text.lower(), name)

    def test_stale_single_pattern_rules_are_gone(self):
        combined = "\n".join(
            (ROOT / ".claude" / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            for name in SKILLS
        )
        self.assertNotIn("Correct Agent Creation Pattern", combined)
        self.assertNotIn("I designed ConnectOnion with 3 main patterns", combined)
        self.assertNotIn("Not setting max_iterations appropriately", combined)

    def test_project_shape_examples_cover_the_decision_boundary(self):
        fixtures = ROOT / "tests" / "fixtures"
        generated = (fixtures / "generated_co_ai.py").read_text()
        direct_factory = (fixtures / "direct_sdk_factory.py").read_text()
        empty = (fixtures / "empty.py").read_text()

        self.assertEqual(classify_project(generated), "generated-co-ai")
        self.assertEqual(classify_project(direct_factory), "direct-sdk")
        self.assertEqual(classify_project(empty, has_host_yaml=True), "generated-project")
        self.assertEqual(classify_project(empty), "unclear")

        for name in SKILLS:
            text = (
                ROOT / ".claude" / "skills" / name / "SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("connectonion.cli.co_ai.agent", text, name)
            self.assertIn("host(create_agent)", text, name)
            self.assertIn(".co/host.yaml", text, name)

    def test_manifest_versions_match(self):
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text()
        )
        plugin = json.loads(
            (ROOT / ".claude-plugin" / "plugin.json").read_text()
        )
        self.assertEqual(marketplace["metadata"]["version"], plugin["version"])
        self.assertEqual(marketplace["plugins"][0]["version"], plugin["version"])


if __name__ == "__main__":
    unittest.main()
