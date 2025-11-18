<div align="center">

# 🧅 ConnectOnion Claude Code Plugin

**Build AI agents correctly, every time.**

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/openonion/connectonion-claude-plugin)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/4xfD9k8AUF)
[![ConnectOnion](https://img.shields.io/badge/ConnectOnion-0.4.2-orange.svg)](https://pypi.org/project/connectonion/)

**[Installation](#installation)** • **[Commands](#commands)** • **[Discord](https://discord.gg/4xfD9k8AUF)** • **[Docs](https://docs.connectonion.com)**

---

</div>

## 🎯 What is This?

The **official Claude Code plugin** for ConnectOnion framework development. Get your code reviewed by **tech legends** - each with their own style:

### 👥 Dual Code Review System

**Choose your reviewer:**

| Reviewer | Style | Focus | Best For |
|----------|-------|-------|----------|
| **Linus** 🔥 | Direct, brutal, no-nonsense | Kill complexity & over-engineering | When your code is too clever |
| **Aaron** 💡 | Thoughtful, educational, constructive | Correctness & elegance | Learning framework patterns |

**Or use both!** Get Linus to kill complexity, then Aaron to polish correctness.

### 🔥 Core Commands
1. **`/linus-review-my-code`** - Get roasted for complexity (Linus-style: direct & honest)
2. **`/aaron-review-my-code`** - Get reviewed by the creator (Aaron: educational & principled)
3. **`/aaron-build-my-agent`** - Let Aaron build your agent (scaffolding done right)

### 🛠️ Development Tools
4. **`/generate-code-map-headers`** - Generate code map headers with dependency analysis and data flow
5. **`/design-refine`** - Iteratively refine website design to professional standards

All commands are grounded in actual ConnectOnion documentation to prevent hallucinations and ensure correctness.

---

## ✨ Why This Plugin?

<table>
<tr>
<td width="33%">

### 🎓 **Educational**
Learn from Aaron, the framework creator. Every review teaches you the "why" behind patterns.

</td>
<td width="33%">

### 🎯 **Accurate**
Grounded in real docs. No hallucinations. Only patterns that actually work.

</td>
<td width="33%">

### ⚡ **Fast**
Review code in seconds. Generate agents in minutes. No memorizing patterns.

</td>
</tr>
</table>

---

## 🚀 Quick Start

**1. Add the marketplace:**
```bash
/plugin marketplace add openonion/connectonion-claude-plugin
```

**2. Install the plugin:**
```bash
/plugin install connectonion
```

**3. Get your first review:**
```bash
/aaron-review-my-code agent.py
```

That's it! 🎉

---

## 💬 Join the Community

[![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Join%20Discord&logo=discord&logoColor=white&style=for-the-badge)](https://discord.gg/4xfD9k8AUF)

Get help, share agents, and discuss with other builders.

---

## 📖 Philosophy

**"Keep simple things simple, make complicated things possible"**

This plugin helps you write ConnectOnion code that follows the framework's philosophy:
- No over-engineering
- Clear, documented patterns
- Simple solutions first
- Complexity only when needed

---

## 📦 Installation

**Method 1: Direct Install (Recommended)**
```bash
# Add marketplace
/plugin marketplace add openonion/connectonion-claude-plugin

# Install plugin
/plugin install connectonion
```

**Method 2: Browse Interactively**
```bash
/plugin
```
Select "Browse Plugins" → Find "connectonion" → Install

---

## 📚 Commands Reference

### `/aaron-review-my-code` - Get Reviewed by the Creator

Get your ConnectOnion code reviewed by Aaron, the framework creator. Principled, educational review focused on correctness and elegance.

**Usage:**

```bash
# Review current file
/aaron-review-my-code

# Review specific file
/aaron-review-my-code path/to/agent.py

# Review entire project
/aaron-review-my-code .
```

**What Aaron Checks:**

✅ **Correctness**
- Proper `Agent()` initialization
- System prompts in markdown files
- Type hints on all tools
- Framework pattern compliance

✅ **Elegance**
- Code simplicity (fighting over-engineering)
- Proper tool patterns (function vs class)
- `llm_do` vs code usage
- Maintainability

✅ **Philosophy Alignment**
- "Keep simple things simple"
- No unnecessary abstractions
- Framework intent honored

**Review Style:**

- **Constructive** - Always teaching, never just criticizing
- **Personal** - From the creator who designed the patterns
- **Educational** - Explains WHY, not just WHAT
- **Community-focused** - Invites you to Discord for help

**Example Output:**

```
💡 Aaron says: agent.py:15

Here's what I'm seeing: Your tool function is missing type hints.

Why this matters: ConnectOnion uses type hints to automatically generate
tool schemas for the LLM. Without them, the agent can't understand what
parameters your tool needs.

Here's how I'd write it:
def search(query: str, limit: int = 10) -> str:
    """Search for information."""
    return f"Results for {query}"

ConnectOnion was designed for: Simple, type-safe tool definitions that
just work without configuration.

📚 Docs: https://docs.connectonion.com/tools/function-tools
```

**At the End:**

Every review ends with:
- Summary of critical vs nice-to-have fixes
- What you're doing right (always positive!)
- Specific next steps with file:line references
- Discord link to get help: https://discord.gg/4xfD9k8AUF
- Personal sign-off from Aaron

**Best for:**
- Learning ConnectOnion patterns from the creator
- Understanding framework philosophy
- Getting constructive, educational feedback
- Joining the community

### `/aaron-build-my-agent` - Let the Creator Build Your Agent

Let Aaron (ConnectOnion creator) build your agent from scratch. He'll ask questions, choose the right pattern, and scaffold complete working code with explanations.

**Usage:**

```bash
/aaron-build-my-agent
```

**Aaron will ask you:**
1. **What should your agent do?** (e.g., "Screenshot websites", "Analyze code")
2. **What operations does it need?** (e.g., "Browser control", "File reading")
3. **Does it need to remember things?** (e.g., "Keep browser session open")

**Then Aaron creates:**

- 🛠️ **Complete agent code** - Ready to run
- 📝 **System prompt file** - In markdown (prompts/[agent_name].md)
- 🎯 **Right pattern** - Simple functions OR class instance based on needs
- ✅ **Proper type hints** - ConnectOnion requires them
- 📚 **Explanation** - Why he built it this way
- 🚀 **Usage instructions** - How to run and customize

**Building Style:**

- **Personal** - From the creator who designed the patterns
- **Educational** - Explains the "why" behind choices
- **Simple first** - Starts with simplest pattern that works
- **Runnable** - Code works immediately
- **Customizable** - Shows how to modify it

**Example Interaction:**

```
User: /aaron-build-my-agent

Aaron: Hey! What should your agent do?

User: Take screenshots of websites

Aaron: Great! Does it need to keep the browser open between screenshots?

User: Yes

Aaron: Perfect! I'll use a class instance pattern for stateful browser control.

[Generates complete browser agent with:
 - BrowserAutomation class
 - System prompt in prompts/web_assistant.md
 - Example usage
 - Explanation of pattern choice]

Aaron: Your agent is ready! I used Pattern B (class instance) because you need
to maintain browser state. The type hints tell ConnectOnion what parameters
each method needs. Check out Discord if you have questions! 🎯
```

**At the end, every generated agent includes:**
- Discord link to get help: https://discord.gg/4xfD9k8AUF
- GitHub issue reporting if something's wrong
- Customization guide
- Personal sign-off from Aaron

**Best for:**
- Building your first agent
- Learning ConnectOnion patterns from the creator
- Getting production-ready scaffolding
- Understanding framework design philosophy

### `/linus-review-my-code` - Get Roasted for Complexity

Get direct, no-nonsense code review from Linus. Hunts down over-engineering and unnecessary complexity with brutal honesty.

**Usage:**

```bash
# Review current file
/linus-review-my-code

# Review specific file
/linus-review-my-code path/to/agent.py

# Review entire project
/linus-review-my-code .
```

**What It Checks:**

🚨 **Over-Engineering Detection**
- Unnecessary try-catch blocks
- Over-abstraction (factories, managers, helpers)
- Utils.py anti-pattern
- Long functions (>40 lines)
- Deep nesting

🚨 **Code Smells**
- Classes that should be functions
- Complex error handling infrastructure
- Unnecessary if-else chains
- Functions that don't fit on one screen

✅ **ConnectOnion Patterns**
- Type hints on tools
- System prompts in files
- Class instance usage
- Proper error handling

**Review Philosophy:**

- **Direct and honest** - Calls out bad code clearly
- **Constructive** - Shows simple solutions
- **Educational** - Explains WHY simplicity matters
- **Focused** - Only flags real problems

**Example Output:**

```
🚨 OVER-ENGINEERING at agent.py:25

Problem: Unnecessary try-catch that hides errors

try:
    result = do_something()
except Exception:
    pass  # This hides errors!

Why this is bad: You just made debugging impossible. If something fails, you WANT to know!

Fix:
result = do_something()  # Let it crash with a clear error message
```

**Best for:**
- Catching over-engineering early
- Learning "keep simple things simple"
- Getting honest feedback on code complexity
- Before committing large features

### `/generate-code-map-headers` - Generate Code Map Headers

Generate code map headers that document dependencies, data flow, and integration points for each file.

**Usage:**

```bash
# Generate headers for all code files
/generate-code-map-headers

# Generate for specific directory or pattern
/generate-code-map-headers src/
/generate-code-map-headers **/*.py
```

**What It Does:**

1. Dependency Analysis
   - Builds import dependency graph
   - Identifies who imports what
   - Detects circular dependencies
   - Finds associated test files

2. Smart Documentation
   - Generates comprehensive file headers
   - Documents data flow and dependencies
   - Lists side effects and state changes
   - Includes integration points

3. Quality Tracking
   - Creates todo list for all files
   - Processes in dependency order (leaves first)
   - Skips already-documented files
   - Reports circular dependencies

**Header Format:**

```python
"""
Purpose: [What problem this solves - one line]
LLM-Note:
  Dependencies: imports from [lib/database.py] | imported by [api/routes.py] | tested by [tests/test_module.py]
  Data flow: receives request_data: Dict → validates → queries database → returns ProcessedResult
  State/Effects: modifies global_cache | writes to PostgreSQL | publishes to Redis
  Integration: exposes process_data() | implements DataProcessor ABC | FastAPI dependency
  Performance: @lru_cache(maxsize=128) | asyncio.gather() | connection pool 10
  Errors: raises ValidationError | @retry(stop_after_attempt=3) | circuit breaker
"""
```

### `/design-refine` - Website Design Analysis

Analyze and iteratively refine website design until it meets professional standards.

**Usage:**

```bash
# Auto-detect running dev server
/design-refine

# Specify URL
/design-refine http://localhost:3000
/design-refine https://mysite.com
```

**What It Does:**

1. Screenshot Capture
   - Full page, mobile, tablet, desktop views
   - Uses `co` command for screenshots

2. Comprehensive Analysis
   - Visual hierarchy (5 levels)
   - Typography scale consistency
   - Spacing system (8px grid)
   - Color harmony and contrast (WCAG AA)
   - Responsive layout at all breakpoints
   - Accessibility compliance
   - Interactive states
   - White space balance

3. Iterative Refinement
   - Creates prioritized fix list (Critical → Low)
   - Fixes issues one by one
   - Captures new screenshots after each fix
   - Re-analyzes for improvements
   - Continues until all Critical/High issues resolved

**Quality Criteria:**
- Clear visual hierarchy
- Consistent 8px spacing
- WCAG AA contrast
- Mobile-responsive
- Professional typography
- Proper interactive states

---

## 🎨 Key Patterns Enforced

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

---

## 🐛 Bug Reports & Feedback

### Found a Problem?

If a command is:
- Stuck in a loop or not completing
- Giving incorrect suggestions
- Missing obvious issues
- Not following documented patterns

**Report it quickly via GitHub CLI:**

```bash
gh issue create --repo openonion/connectonion-claude-plugin \
  --title "[command-name]: [brief issue]" \
  --body "Command: /command-name

Problem: [what went wrong]
Expected: [what should happen]
File: [if applicable]

Code context:
\`\`\`python
[paste code if relevant]
\`\`\`"
```

**Or report manually:**
- **GitHub Issues**: https://github.com/openonion/connectonion-claude-plugin/issues
- **Discord**: https://discord.gg/4xfD9k8AUF

Your feedback makes the plugin better for everyone! 🙏

---

## 🤝 Contributing

Want to improve the plugin?

1. **Fork**: https://github.com/openonion/connectonion-claude-plugin
2. **Issues**: Report bugs or request features
3. **Pull Requests**: Submit improvements
4. **Discord**: Discuss ideas at https://discord.gg/4xfD9k8AUF

---

## ⭐ Show Your Support

If this plugin helps you build better agents, **give it a star!** ⭐

It helps others discover the plugin and motivates us to keep improving it.

---

## 📄 License

Apache-2.0

---

## 🔗 Links

- **ConnectOnion Docs**: https://docs.connectonion.com
- **GitHub**: https://github.com/openonion/connectonion
- **PyPI**: https://pypi.org/project/connectonion/
- **Discord**: https://discord.gg/4xfD9k8AUF

---

<div align="center">

**Made with ❤️ by the ConnectOnion Team**

[⭐ Star this repo](https://github.com/openonion/connectonion-claude-plugin) • [💬 Join Discord](https://discord.gg/4xfD9k8AUF) • [📖 Read Docs](https://docs.connectonion.com)

</div>