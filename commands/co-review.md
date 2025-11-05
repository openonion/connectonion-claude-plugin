---
description: Review code against ConnectOnion documentation and best practices
---

# ConnectOnion Code Review

You are reviewing code to ensure it follows **documented ConnectOnion patterns**. Every recommendation must be based on actual framework documentation, not assumptions.

## Core Philosophy (From Documentation)

**"Keep simple things simple, make complicated things possible"**

This means:
- Avoid over-engineering
- No unnecessary abstractions
- Simple code is better than clever code
- Only add complexity when needed

## Step 1: Read the Code

Use Read or Glob tools to examine the files being reviewed.

## Step 2: Check Against Documentation

Review code against these **documented patterns from ConnectOnion**:

### ✅ Correct Agent Creation Pattern

```python
# DOCUMENTED PATTERN: Simple 2-line agent usage
from connectonion import Agent

agent = Agent(
    name="assistant",
    system_prompt="prompts/assistant.md",  # Use markdown files!
    tools=[search, calculate],
    max_iterations=10  # Default is 10
)

result = agent.input("What is 25 * 4?")
```

**Common mistakes:**
- ❌ Inline string prompts (should use markdown files)
- ❌ Not setting max_iterations appropriately
- ❌ Missing clear agent name

### ✅ Function-Based Tools (RECOMMENDED)

```python
# DOCUMENTED PATTERN: Function tools with type hints
def search(query: str, limit: int = 10) -> str:
    """Search for information."""
    return f"Found {limit} results for {query}"

# Pass function directly
agent = Agent("assistant", tools=[search])
```

**Required by documentation:**
- ✅ Type hints on all parameters
- ✅ Type hint on return value
- ✅ Docstring (becomes tool description)
- ✅ Default values for optional params

**Common mistakes:**
- ❌ Missing type hints: `def search(query, limit=10):`
- ❌ No docstring
- ❌ Vague return types

### ✅ Class Instance Tools (For Stateful Tools)

```python
# DOCUMENTED PATTERN: Pass entire class instance
class BrowserAutomation:
    def __init__(self):
        self._page = None

    def start_browser(self, headless: bool = True) -> str:
        """Start a Chromium browser session."""
        # Implementation
        return "Browser started"

    def goto(self, url: str) -> str:
        """Navigate to a URL and return the page title."""
        # Implementation
        return "Page title"

# ✅ CORRECT: Pass instance directly (auto-discovers methods)
browser = BrowserAutomation()
agent = Agent("web_agent", tools=[browser])

# ❌ WRONG: Listing methods individually
agent = Agent("web_agent", tools=[
    browser.start_browser,
    browser.goto,
    # ... manual listing (verbose and error-prone)
])
```

**Documentation says:**
> "✅ RECOMMENDED: Pass the class instance directly to ConnectOnion!"
> "ConnectOnion automatically discovers all public methods with type hints when you pass a class instance."

### ✅ System Prompts (Use Markdown Files)

```python
# ✅ RECOMMENDED by documentation
agent = Agent(
    name="support_agent",
    system_prompt="prompts/customer_support.md",
    tools=[create_ticket]
)

# ❌ AVOID: Inline strings (hard to maintain)
agent = Agent(
    name="support_agent",
    system_prompt="You are a support agent. Be helpful...",  # Don't do this!
    tools=[create_ticket]
)
```

**Documentation says:**
> "Best Practice: Use Markdown Files for System Prompts"
> "Keep your prompts separate from code for better maintainability"

**Only acceptable inline:** Very simple one-line prompts

### ✅ llm_do vs Code (When to Use Each)

```python
from connectonion import llm_do
from pydantic import BaseModel

# ✅ Use llm_do for natural language tasks
class EmailDraft(BaseModel):
    subject: str
    body: str

draft = llm_do(
    "Write an email thanking the team",
    output=EmailDraft
)

# ✅ Use code for deterministic tasks
def calculate_total(items: list) -> float:
    return sum(item.price for item in items)
```

**Documentation says:**
> "Use LLMs for language, Code for logic"

**Use llm_do for:**
- Natural language generation (emails, summaries)
- Content understanding and extraction
- Translation and transformation

**Use code for:**
- Math calculations
- Database queries
- Date formatting
- Validation logic

### ✅ max_iterations Guidelines

```python
# Documentation guidelines:
simple_agent = Agent("calc", tools=[calculate], max_iterations=5)      # Simple tasks: 3-5
standard_agent = Agent("helper", tools=[...], max_iterations=10)       # Default: 10
complex_agent = Agent("research", tools=[...], max_iterations=25)      # Complex: 20-40
```

**Documentation says:**
> "Default: 10 iterations (good for most tasks)"

### ✅ Debugging with @xray

```python
from connectonion.decorators import xray

@xray
def my_tool(text: str) -> str:
    """Process text."""
    # Access debugging context
    print(xray.agent.name)     # Agent calling this tool
    print(xray.task)           # User's request
    print(xray.iteration)      # Current iteration
    print(xray.previous_tools) # Tools called before

    return f"Processed: {text}"
```

**Documentation says:**
> "Debug your agent's tool execution with real-time insights"

## Step 3: Check for Anti-Patterns

### ❌ Over-Engineering

```python
# ❌ BAD: Unnecessary abstraction
class ToolFactory:
    def create_tool(self, type: str):
        if type == "search":
            return SearchTool()
        # Complex factory pattern not needed

# ✅ GOOD: Just use functions
def search(query: str) -> str:
    """Search for information."""
    return f"Results for {query}"
```

### ❌ Missing Type Hints

```python
# ❌ BAD: No type hints (will not work correctly)
def search(query, limit=10):
    return "results"

# ✅ GOOD: Proper type hints (required by ConnectOnion)
def search(query: str, limit: int = 10) -> str:
    return "results"
```

### ❌ Listing Methods Instead of Instance

```python
# ❌ BAD: Manual method listing (verbose)
browser = BrowserAutomation()
agent = Agent("web", tools=[
    browser.start,
    browser.goto,
    browser.screenshot
])

# ✅ GOOD: Pass instance (auto-discovery)
browser = BrowserAutomation()
agent = Agent("web", tools=[browser])
```

## Step 4: Review Output Format

For each issue found, provide:

```
❌ [Issue Type] at file.py:line_number

Problem: [What's wrong]

Documentation Reference: [Quote or cite the ConnectOnion docs]

Why it matters: [Explain the principle]

Suggested Fix:
[Show correct code]

Example from docs:
[Show relevant documented pattern]
```

For good code:

```
✅ Good Pattern at file.py:line_number

What's correct: [What's done well]

Documentation reference: [What pattern it follows]
```

## Step 5: Provide Summary

At the end, summarize:

1. **Critical Issues** - Must fix (breaks framework patterns)
2. **Improvements** - Should fix (better practices)
3. **Good Patterns** - What's working well
4. **Documentation Links** - Relevant sections to review

## Important Reminders

1. **Reference Documentation** - Every recommendation must cite documented patterns
2. **Don't Hallucinate** - If unsure, say "This pattern is not documented"
3. **Be Educational** - Explain why patterns matter
4. **Show Examples** - Use actual documented examples
5. **Focus on Philosophy** - "Keep simple things simple"

## What NOT to Review

- Don't review business logic correctness (that's domain-specific)
- Don't review algorithm efficiency (unless obviously wrong)
- Focus only on ConnectOnion framework usage patterns

Now review the code following this structure!
