---
description: Build or specialize a ConnectOnion agent using the project's current architecture
---

# Build my ConnectOnion agent

Build the smallest working change for the project that is actually open. Do
not replace a current ConnectOnion scaffold with an older example shape.

## 1. Identify the project shape

Read `agent.py`, `.co/host.yaml`, `.co/docs/README.md`, and existing
`.co/skills/*/SKILL.md` files when they exist.

Use positive evidence in this order:

1. An exact import from `connectonion.cli.co_ai.agent` plus `host(...)` is a
   generated **co-ai project**. Its intended shape is:

```python
from connectonion import host
from connectonion.cli.co_ai.agent import create_agent

agent = create_agent(role="coding")
host(agent)
```

2. Otherwise, an existing `Agent(...)` or `llm_do(...)` composition is a
   **direct SDK project**. A project-local function named `create_agent` passed
   to `host(create_agent)` is a supported direct SDK factory, not co-ai.
3. Otherwise, `.co/host.yaml` identifies a generated ConnectOnion project whose
   entrypoint may be incomplete; preserve it and establish the intended
   generated shape before editing.
4. With none of that evidence, the shape is unclear. Ask whether to run the
   current `co create` path or build a direct SDK application.

Never mix both shapes in one project by accident.

## 2. Build in a generated co-ai project

The agent already has files, shell, browser, planning, todos, sub-agents, and
skill discovery. Specialize its procedure, not its wiring.

1. Read the relevant pages under `.co/docs/`, including design decisions for
   framework-wide choices.
2. Ask only for missing product behavior or an external dependency that
   materially changes the design.
3. Create or refine `.co/skills/<skill-name>/SKILL.md`:

```markdown
---
name: skill-name
description: What this skill does and when to use it.
---

# Skill title

## Instructions

1. Read the necessary context.
2. Perform the procedure in an explicit order.
3. Validate the outcome and report failures honestly.

## Safety

- Name irreversible actions and require normal approval.
- Never place credentials in the skill or output.
```

4. Keep `agent.py` unchanged unless the user explicitly requests a role or
   hosting change. Do not manually add tools the co-ai agent already owns.
5. Add deterministic code beside the skill only when the procedure genuinely
   needs it. Keep policy and sequencing in the skill; keep deterministic logic
   in code.
6. Test skill discovery and any deterministic code offline.

If the requested capability needs a new Python tool or a different runtime
composition, say so. Discuss a direct SDK/custom project instead of silently
turning the generated co-ai template into one.

## 3. Build in a direct SDK project

Preserve the project's existing lifecycle and style. Read local docs first.

- Prefer a typed function for stateless operations.
- Pass an instance when several methods share real state.
- Give tools focused docstrings because they become model-facing schemas.
- Keep long prompts in markdown when that improves maintenance; a short
  literal prompt is valid.
- Set model and iteration limits only when the task needs non-default values.
- Keep `input()` for local execution and `host()` for a hosted entrypoint; do
  not add both without a reason.

Example direct SDK shape:

```python
from connectonion import Agent


def lookup(topic: str) -> str:
    """Look up one topic."""
    return topic


agent = Agent("researcher", tools=[lookup])
print(agent.input("Find the release notes"))
```

## 4. Validate and deliver

- Run the smallest relevant tests, then the repository check required for the
  touched surface.
- Read the final diff and remove accidental complexity.
- Report files changed, checks run, and any decision the user still owns.
- Do not commit, push, deploy, or publish unless the user asked.

The skill supplies procedure, not authority. All file, shell, git, network,
and deployment actions still follow Claude Code's normal permission model.
