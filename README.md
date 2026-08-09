# ConnectOnion Claude Code plugin

The official Claude Code plugin for building and reviewing ConnectOnion
projects without losing the project's current architecture.

## Install

Run these commands inside Claude Code:

```text
/plugin marketplace add openonion/connectonion-claude-plugin
/plugin install connectonion@connectonion-marketplace
/reload-plugins
```

Claude Code namespaces installed skills with the plugin name.

## Skills

### `/connectonion:aaron-build-my-agent`

Builds or specializes an agent after detecting its project shape.

- In a generated `co-ai` project, it reads `.co/docs/`, keeps the small
  `create_agent(...) + host(...)` entrypoint, and puts specialized procedures
  in `.co/skills/<name>/SKILL.md`.
- In a direct SDK project, it preserves the existing `Agent(...)` lifecycle
  and uses typed functions or stateful instances where appropriate.

### `/connectonion:aaron-review-my-code`

Reviews correctness before style, using local `.co/docs/` as the
framework-version source of truth. It applies separate checklists to generated
`co-ai` projects and direct SDK applications.

```text
/connectonion:aaron-review-my-code .
```

### `/connectonion:linus-review-my-code`

Reviews for accidental complexity and proposes the smallest correction that
preserves the real contract. It does not treat the generated `co-ai` scaffold
as missing explicit tools or configuration.

```text
/connectonion:linus-review-my-code .
```

### Other skills

- `/connectonion:generate-code-map-headers`
- `/connectonion:design-refine`
- `/connectonion:diagram`

Use `/plugin` to view the current installed catalog.

## The two supported project shapes

### Generated co-ai project

`co create` produces one small, deployable agent:

```python
from connectonion import host
from connectonion.cli.co_ai.agent import create_agent

agent = create_agent(role="coding")
host(agent)
```

Do not expand this file with tools the co-ai agent already owns. Specialize
behavior with project skills in `.co/skills/`; change `role` only when the
domain changes.

### Direct SDK project

Direct SDK applications remain valid when a project needs its own agent
composition:

```python
from connectonion import Agent


def search(query: str) -> str:
    """Search for one query."""
    return query


agent = Agent("researcher", tools=[search])
print(agent.input("Find the release notes"))
```

The plugin detects the shape before building or reviewing. It does not convert
one shape into the other without an explicit request.

## Documentation and permissions

When `.co/docs/` exists, the skills read it before making
ConnectOnion-specific claims. That keeps advice aligned with the framework
version installed in the project.

Plugin skills provide procedures, not authority. File edits, shell commands,
git writes, network calls, and deployments still use Claude Code's normal
permission model.

## Development

Validate the marketplace and contract tests before opening a PR:

```bash
claude plugin validate .
python -m unittest discover -s tests
```

Report plugin problems at
[openonion/connectonion-claude-plugin](https://github.com/openonion/connectonion-claude-plugin/issues).

ConnectOnion documentation: <https://docs.connectonion.com>

License: Apache-2.0
