# ConnectOnion Claude Code Plugin

Official Claude Code plugin for ConnectOnion framework development. Build AI agents correctly, every time.

## What is This?

This plugin provides two essential commands for ConnectOnion developers:

1. **`/co-review`** - Review code against ConnectOnion documentation and best practices
2. **`/co-build`** - Build ConnectOnion agents following documented patterns

Both commands are grounded in actual ConnectOnion documentation to prevent hallucinations and ensure correctness.

## Philosophy

**"Keep simple things simple, make complicated things possible"**

This plugin helps you write ConnectOnion code that follows the framework's philosophy:
- No over-engineering
- Clear, documented patterns
- Simple solutions first
- Complexity only when needed

## Installation

### Add the Marketplace

```bash
/plugin marketplace add openonion/connectonion-claude-plugin
```

### Install the Plugin

```bash
/plugin install connectonion
```

Or browse plugins interactively:

```bash
/plugin
```

Select "Browse Plugins" and install `connectonion`.

## Commands

### `/co-review` - Code Review

Review your ConnectOnion code against framework documentation.

**Usage:**

```bash
# Review current file
/co-review

# Review specific file
/co-review path/to/agent.py

# Review entire project
/co-review .
```

**What It Checks:**

✅ **Agent Creation Patterns**
- Proper `Agent()` initialization
- System prompts in markdown files
- Appropriate `max_iterations`

✅ **Tool Patterns**
- Function-based tools with type hints
- Class instance tools (pass instance, not methods)
- Proper docstrings

✅ **Best Practices**
- `llm_do` vs code usage
- No over-engineering
- Documentation compliance

**Example Output:**

```
❌ Missing Type Hints at agent.py:15

Problem: Tool function missing required type hints

Documentation Reference: "Type hints are required on all parameters and return"

Suggested Fix:
# Before
def search(query, limit=10):
    return "results"

# After
def search(query: str, limit: int = 10) -> str:
    return "results"
```

### `/co-build` - Agent Builder

Build ConnectOnion agents interactively following documented patterns.

**Usage:**

```bash
/co-build
```

The command will ask you:
1. What should your agent do?
2. What tools does it need?
3. Does it need shared state?

Then generates complete, working code.

**Generated Code Includes:**

- ✅ Complete imports
- ✅ Tool definitions with proper type hints
- ✅ System prompt file template
- ✅ Agent configuration
- ✅ Example usage
- ✅ Inline documentation

**Example Interaction:**

```
User: /co-build
Agent: What should your agent do?
User: Take screenshots of websites
Agent: [Generates complete browser agent code with proper patterns]
```

## Why Use This Plugin?

### 1. Documentation-Grounded

Every recommendation and code pattern comes from actual ConnectOnion documentation. No hallucinations.

### 2. Correct by Design

Generated code follows framework best practices:
- Type hints required
- Proper class instance usage
- Markdown system prompts
- Appropriate `max_iterations`

### 3. Educational

Explains **why** patterns matter, not just what to fix. References documentation sections for learning.

### 4. Time-Saving

- Review code in seconds
- Generate working agents in minutes
- No need to remember all patterns

## Key Patterns Enforced

### Function-Based Tools (Recommended)

```python
# ✅ Correct
def search(query: str, limit: int = 10) -> str:
    """Search for information."""
    return f"Found {limit} results"

agent = Agent("assistant", tools=[search])
```

### Class Instance Tools (For State)

```python
# ✅ Correct - pass instance
browser = BrowserAutomation()
agent = Agent("web", tools=[browser])  # Auto-discovers methods!

# ❌ Wrong - don't list methods
agent = Agent("web", tools=[browser.start, browser.goto, ...])  # Verbose!
```

### System Prompts in Files

```python
# ✅ Correct - markdown file
agent = Agent(
    name="assistant",
    system_prompt="prompts/assistant.md",  # Maintainable
    tools=[...]
)

# ❌ Wrong - inline string (unless very simple)
agent = Agent(
    name="assistant",
    system_prompt="You are an assistant...",  # Hard to maintain
    tools=[...]
)
```

## Documentation References

This plugin enforces patterns from:
- ConnectOnion Framework Documentation
- Official Examples
- Best Practices Guide

All recommendations cite specific documentation sections.

## Contributing

Found an issue or want to improve the plugin?

1. **GitHub**: https://github.com/openonion/connectonion-claude-plugin
2. **Issues**: Report bugs or request features
3. **Discord**: Join our community at https://discord.gg/4xfD9k8AUF

## License

Apache-2.0

## Links

- **ConnectOnion Docs**: https://docs.connectonion.com
- **GitHub**: https://github.com/openonion/connectonion
- **PyPI**: https://pypi.org/project/connectonion/
- **Discord**: https://discord.gg/4xfD9k8AUF

---

Made with ❤️ by the ConnectOnion Team