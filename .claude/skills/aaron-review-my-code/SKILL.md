---
description: Review ConnectOnion code against the project's actual architecture and local docs
---

# Aaron review

Review for correctness first, then simplicity. Ground framework claims in the
project's `.co/docs/` when available; do not impose an older ConnectOnion
example on a newer project.

## 1. Establish the contract

1. Read the requested files, their callers, tests, and current diff.
2. State the user-facing behavior in one sentence.
3. Read `.co/docs/README.md` and relevant design decisions for
   framework-specific changes.
4. Identify the project shape before judging agent construction. Use the
   exact `connectonion.cli.co_ai.agent` import as co-ai evidence. Otherwise an
   existing `Agent(...)` or `llm_do(...)` composition, including a local
   `create_agent` factory passed to `host(create_agent)`, is direct SDK. If
   neither exists but `.co/host.yaml` does, preserve it as a generated project
   with an incomplete or modified entrypoint. With no positive evidence, ask;
   do not choose an architecture silently.

### Generated co-ai project

`agent.py` composes `create_agent(...)` and `host(...)`. This is correct:

```python
from connectonion import host
from connectonion.cli.co_ai.agent import create_agent

agent = create_agent(role="coding")
host(agent)
```

Do **not** require an explicit agent name, tools list, prompt file, or
`max_iterations` in this shape. The SDK owns the shared agent composition.
Project behavior belongs primarily in `.co/skills/<name>/SKILL.md`; the role
supplies domain doctrine.

Review this shape for:

- a small composition-only `agent.py`;
- an appropriate `role` and one hosted lifecycle;
- valid skill frontmatter and clear, bounded procedures;
- deterministic policy before model judgment where possible;
- no secrets or machine-specific paths in skills;
- tests for discovery and deterministic helpers;
- deployment truth in `.co/host.yaml` and project-local skill paths.

### Direct SDK project

The project constructs `Agent(...)` or `llm_do(...)` directly. Review the
existing design rather than converting it to co-ai without a request.

Review this shape for:

- typed, documented function tools for stateless work;
- instances only when methods share real state;
- prompt placement that matches its size and reuse;
- explicit lifecycle: local `input()` or hosted `host()` as intended;
- non-default model/iteration settings only when justified;
- deterministic code for logic and LLMs for language judgment.

## 2. Look for real failures

Prioritize:

1. incorrect behavior or broken lifecycle;
2. security, permission, credential, and irreversible-action mistakes;
3. swallowed errors and false success;
4. API/CLI contract drift;
5. compatibility and missing failure-mode tests;
6. unnecessary abstractions or duplicated sources of truth.

Do not invent requirements from style preferences. A short literal prompt is
not automatically wrong. A default iteration limit is not automatically
missing. Tests are valuable when they defend behavior, not implementation
ceremony.

## 3. Report findings first

Order findings by severity. Each finding must include:

- `file:line` evidence;
- the concrete failure or maintenance cost;
- the smallest viable correction;
- the relevant local documentation when the claim is ConnectOnion-specific.

If there are no material findings, say so explicitly and name residual risks
or validation gaps. Keep praise and summaries after findings.

## 4. Review boundaries

- Review does not authorize edits, commits, pushes, comments, or merges.
- Never expose `.env`, credentials, tokens, or private-key material.
- Ask before expanding from the requested files into a different architecture.
- If local docs conflict with this skill, report the drift and follow the
  project's versioned docs.
