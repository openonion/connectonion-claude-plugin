# ConnectOnion Claude Code Plugin

Official Claude Code plugin for ConnectOnion framework development. Build AI agents correctly, every time.

## What is This?

This plugin provides essential commands for ConnectOnion framework development:

### Core Development Commands
1. **`/co-review`** - Review code against ConnectOnion documentation and best practices
2. **`/co-build`** - Build ConnectOnion agents following documented patterns

### Project Management Commands
3. **`/release`** - Automate version release - update version, build, publish to PyPI, create GitHub release
4. **`/update-docs`** - Update all documentation for a feature with deep understanding first
5. **`/wiki-sync`** - AI-driven wiki content synthesis from docs/ with SEO optimization

### Development Tools
6. **`/migrate-to-ts`** - Migrate one Python ConnectOnion feature to TypeScript version
7. **`/code-analyze-doc`** - Analyze code structure and add documentation headers to each file
8. **`/design-refine`** - Analyze and iteratively refine website design until it meets professional standards

All commands are grounded in actual ConnectOnion documentation to prevent hallucinations and ensure correctness.

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

### `/release` - Version Release Automation

Automate the complete release workflow including version bumping, PyPI publishing, GitHub releases, and documentation updates.

**Usage:**

```bash
# Automatic version detection from commit history
/release auto

# Explicit PATCH bump (bug fixes, docs)
/release patch

# Explicit MINOR bump (new features)
/release minor

# Explicit MAJOR bump (breaking changes)
/release major
```

**What It Does:**

1. Version Management
   - Bumps version following VERSIONING.md rules
   - Updates `__init__.py`, `setup.py`, `VERSIONING.md`
   - Creates annotated git tags

2. Publishing
   - Builds wheel and source distributions
   - Uploads to PyPI
   - Verifies installation

3. GitHub Integration
   - Creates GitHub releases with generated notes
   - Posts discussion announcement (GraphQL)
   - Sends Discord webhook notification

4. Documentation
   - Updates docs site version badges
   - Rebuilds documentation if needed

### `/update-docs` - Feature Documentation

Update all documentation for a feature with deep understanding first.

**Usage:**

```bash
/update-docs <feature-name>

# Example
/update-docs auto_debug
```

**What It Does:**

1. Deep Understanding
   - Reads implementation code
   - Reviews existing documentation
   - Analyzes examples and tests
   - Identifies user pain points

2. Comprehensive Updates
   - Updates main docs (`docs/`)
   - Creates/updates GitHub wiki pages
   - Updates docs site navigation and pages
   - Updates README and quickstart
   - Updates CLI embedded docs

3. Quality Verification
   - Tests all code examples
   - Verifies all links
   - Ensures mobile-friendly design
   - Commits to nested repos correctly

### `/wiki-sync` - Wiki Content Synthesis

AI-driven wiki content synthesis from docs/ with SEO optimization (comprehension-based, not copy-paste).

**Usage:**

```bash
# Focus on recently changed docs (default)
/wiki-sync focus-recent

# Comprehensive update of entire wiki
/wiki-sync full-sync

# Create new wiki pages for uncovered topics
/wiki-sync new-topics
```

**What It Does:**

1. Content Analysis
   - Discovers recent documentation changes
   - Reads and comprehends all docs
   - Identifies gaps in wiki coverage
   - Researches SEO keywords

2. AI-Driven Synthesis
   - Creates beginner-friendly content from understanding
   - Applies SEO template structure
   - Adds working code examples with output
   - Includes common issues and solutions

3. SEO Optimization
   - Targets high-volume keywords
   - Question-format headings
   - Internal cross-linking
   - 1000-2000 word count per page

### `/migrate-to-ts` - Python to TypeScript Migration

Migrate one Python ConnectOnion feature to TypeScript version following the "keep it simple" philosophy.

**Usage:**

```bash
/migrate-to-ts <feature-description-or-file:line>

# Examples
/migrate-to-ts docs/examples/search_tool.py
/migrate-to-ts "search agent with calculator"
```

**What It Does:**

1. Reading Phase
   - Reads Python source files
   - Reads related imports and dependencies
   - Reviews TypeScript SDK patterns
   - Creates detailed todo list

2. Direct Translation
   - Simple syntax conversion (no over-engineering)
   - Preserves original behavior
   - NO try-catch unless Python had it
   - NO abstractions that didn't exist

3. Testing
   - Copies .env from examples
   - Creates simple test file
   - Runs tests to verify behavior

**Key Principles:**
- Less code = better code
- Don't make user learn new things
- Let it crash (no unnecessary error handling)
- 5 lines Python = 5 lines TypeScript

### `/code-analyze-doc` - Code Documentation Headers

Analyze code structure and add comprehensive documentation headers to each file.

**Usage:**

```bash
# Analyze all code files
/code-analyze-doc

# Analyze specific directory or pattern
/code-analyze-doc src/
/code-analyze-doc **/*.py
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