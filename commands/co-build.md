---
description: Build ConnectOnion agents following documented patterns
---

# ConnectOnion Agent Builder

Help users build ConnectOnion agents that follow **documented framework patterns**. Generate code that exactly matches the official documentation.

## Philosophy

**"Keep simple things simple, make complicated things possible"**

Start with the simplest working code, add complexity only when needed.

## Step 1: Understand the Requirement

Ask the user what their agent should do. Be specific:

1. **What is the agent's purpose?** (e.g., "Take screenshots", "Search and summarize")
2. **What tools does it need?** (e.g., "Browser automation", "File operations")
3. **Is state needed?** (e.g., "Browser session across calls")

## Step 2: Choose the Right Pattern

Based on requirements, choose the documented pattern:

### Pattern A: Simple Agent (Function Tools)

**Use when:** Agent needs simple, stateless tools

**Documented Pattern:**
```python
from connectonion import Agent

# Define tools as functions
def search(query: str, limit: int = 10) -> str:
    """Search for information."""
    # Implementation
    return f"Found {limit} results for {query}"

def calculate(expression: str) -> float:
    """Perform mathematical calculations."""
    # Implementation
    return eval(expression)  # Use safely in production

# Create agent
agent = Agent(
    name="assistant",
    system_prompt="prompts/assistant.md",
    tools=[search, calculate],
    max_iterations=10
)

# Use agent
result = agent.input("Search for Python tutorials and count how many")
print(result)
```

**Key Requirements (from docs):**
- ✅ Type hints required on all parameters and return
- ✅ Docstrings become tool descriptions
- ✅ Default values for optional parameters
- ✅ System prompt in markdown file

### Pattern B: Stateful Agent (Class Instance Tools)

**Use when:** Tools need shared state (browser session, database connection, cache)

**Documented Pattern:**
```python
from connectonion import Agent

class BrowserAutomation:
    """Browser automation with shared session state."""

    def __init__(self):
        self._browser = None
        self._page = None

    def start_browser(self, headless: bool = True) -> str:
        """Start a Chromium browser session."""
        from playwright.sync_api import sync_playwright
        self._p = sync_playwright().start()
        self._browser = self._p.chromium.launch(headless=headless)
        self._page = self._browser.new_page()
        return f"Browser started (headless={headless})"

    def goto(self, url: str) -> str:
        """Navigate to a URL and return the page title."""
        if not self._page:
            return "Error: Browser not started"
        self._page.goto(url)
        return self._page.title()

    def screenshot(self, filename: str = "page.png") -> str:
        """Save a screenshot and return the filename."""
        if not self._page:
            return "Error: Browser not started"
        self._page.screenshot(path=filename)
        return filename

    def close(self) -> str:
        """Close browser and clean up resources."""
        if self._page:
            self._page.close()
        if self._browser:
            self._browser.close()
        if self._p:
            self._p.stop()
        return "Browser closed"

# ✅ CRITICAL: Pass class instance directly
# ConnectOnion auto-discovers all public methods
browser = BrowserAutomation()
agent = Agent(
    name="web_assistant",
    system_prompt="prompts/web_assistant.md",
    tools=[browser],  # Pass instance, not individual methods!
    max_iterations=15
)

result = agent.input("Go to example.com and take a screenshot")
```

**Documentation says:**
> "✅ RECOMMENDED: Pass the class instance directly to ConnectOnion!"
> "ConnectOnion automatically discovers all public methods with type hints"

### Pattern C: Mixed Tools (Functions + Class Instance)

**Use when:** Need both stateful and utility functions

**Documented Pattern:**
```python
from connectonion import Agent

# Class for stateful operations
class BrowserAutomation:
    # ... (methods as above)

# Function for simple utilities
def format_title(title: str) -> str:
    """Format a page title for logs or UIs."""
    return f"[PAGE] {title}"

# Mix both types
browser = BrowserAutomation()
agent = Agent(
    name="web_assistant",
    system_prompt="prompts/web_assistant.md",
    tools=[browser, format_title],  # Class instance + function
    max_iterations=15
)
```

**Documentation says:**
> "Mix class instance + functions"

## Step 3: Generate System Prompt File

**Always create a markdown file for system prompts** (documented best practice)

Create `prompts/{agent_name}.md`:

```markdown
# {Agent Name}

You are a {description of agent's role}.

## Your Capabilities
- {List what the agent can do}
- {Based on tools provided}

## Guidelines
1. {Behavioral guideline}
2. {When to use which tools}
3. {How to respond to users}

## Tone
- {Personality traits}
- {Communication style}
```

**Documentation says:**
> "Best Practice: Use Markdown Files for System Prompts"
> "Keep your prompts separate from code for better maintainability"

## Step 4: Set Appropriate max_iterations

**Documented Guidelines:**

```python
# Simple tasks (calculation, single search)
agent = Agent("calc", tools=[...], max_iterations=5)

# Standard tasks (most use cases)
agent = Agent("helper", tools=[...], max_iterations=10)  # Default

# Complex tasks (research, multi-step analysis)
agent = Agent("researcher", tools=[...], max_iterations=25)
```

**Documentation says:**
> "Simple tasks: 3-5 iterations"
> "Standard workflows: 10-15 iterations"
> "Complex analysis: 20-40 iterations"

## Step 5: Add Debugging (Optional)

**For development, suggest @xray decorator:**

```python
from connectonion.decorators import xray

@xray
def search(query: str) -> str:
    """Search for information."""
    # Can now access debugging context
    print(f"Called in iteration: {xray.iteration}")
    print(f"User task: {xray.task}")
    return f"Results for {query}"
```

## Step 6: Generate Complete Working Code

Provide a **complete, runnable** example:

1. **All imports** at the top
2. **Tool definitions** (functions or class)
3. **Agent creation** with proper configuration
4. **Example usage** showing how to run it
5. **Comments** explaining key parts

### Example Output Format:

```python
"""
{Agent Name} - {Brief Description}

Purpose: {What this agent does}
Tools: {List of tools}
"""

from connectonion import Agent

# Tool definitions
def tool_name(param: str) -> str:
    """Tool description."""
    # Implementation
    return result

# Create system prompt file (prompts/{name}.md)
# [Show what should be in the markdown file]

# Create agent
agent = Agent(
    name="{agent_name}",
    system_prompt="prompts/{agent_name}.md",
    tools=[tool_name],
    max_iterations=10  # Adjust based on complexity
)

# Example usage
if __name__ == "__main__":
    result = agent.input("Example task")
    print(result)
```

## Common Mistakes to Avoid

### ❌ DON'T: List methods individually
```python
browser = BrowserAutomation()
agent = Agent("web", tools=[
    browser.start_browser,
    browser.goto,
    browser.screenshot  # Verbose and error-prone
])
```

### ✅ DO: Pass class instance
```python
browser = BrowserAutomation()
agent = Agent("web", tools=[browser])  # Auto-discovers methods!
```

### ❌ DON'T: Inline system prompts (unless very simple)
```python
agent = Agent(
    name="assistant",
    system_prompt="You are an assistant. Be helpful. Be clear. Ask questions...",  # Too long!
    tools=[...]
)
```

### ✅ DO: Use markdown files
```python
agent = Agent(
    name="assistant",
    system_prompt="prompts/assistant.md",  # Clean separation
    tools=[...]
)
```

### ❌ DON'T: Missing type hints
```python
def search(query, limit=10):  # Will not work correctly!
    return "results"
```

### ✅ DO: Include all type hints
```python
def search(query: str, limit: int = 10) -> str:  # Required by framework
    return "results"
```

## Step 7: Explain the Code

After generating code, explain:

1. **Why this pattern?** - Connect to documented practices
2. **How to run it?** - Clear instructions
3. **How to customize?** - What can be changed
4. **Next steps?** - How to extend or deploy

## Important Principles

1. **Reference Documentation** - Everything must follow documented patterns
2. **No Hallucination** - Only use documented features
3. **Keep It Simple** - Start minimal, user can add complexity
4. **Working Code** - Must be runnable as-is
5. **Educational** - Explain why patterns are used

## Questions to Ask User

Before generating, confirm:

1. **Purpose**: "What should your agent do?"
2. **Tools needed**: "What operations does it need?" (list common tools)
3. **Statefulness**: "Do tools need to share state?" (e.g., browser session)
4. **Complexity**: "Simple task or multi-step workflow?" (affects max_iterations)

Now help the user build their ConnectOnion agent following these documented patterns!
