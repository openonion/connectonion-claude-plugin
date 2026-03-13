---
allowed-tools: Read, Glob, Grep, Write
description: Analyze code and draw ASCII diagram to explain lifecycle and flow
argument-hint: <file-or-directory>
---

# Code Flow Diagram - Make Code Easy to Understand

You're reading code and feeling lost? This skill reads the code for you and draws simple diagrams that explain:
- **What happens when** - The step-by-step flow
- **How things connect** - Which parts talk to each other
- **Where data goes** - How information transforms through the code
- **The big picture** - Overall architecture at a glance

## Quick Start

```bash
# Understand a file
/diagram src/agent.py

# Focus on specific functionality
/diagram src/agent.py "how does tool execution work?"

# Understand a whole module
/diagram src/tools/
```

## What You Get - 4 Clear Sections

Every diagram includes:

### 1. 📋 **Overview** - What is this code?
One-line summary + main purpose + key components

### 2. 🔄 **Lifecycle** - What happens step-by-step?
Visual flow from start to finish with numbered steps

### 3. 🔍 **Key Concepts** - What's important to know?
Important patterns, gotchas, and design decisions

### 4. 📦 **Dependencies** - What does it need?
External imports and internal modules it relies on

## Real Example - Understanding agent.py

```
================================================================================
FILE: agent.py
PURPOSE: Main Agent class that coordinates LLM calls and tool execution
================================================================================

📋 OVERVIEW
───────────
The Agent class is the heart of ConnectOnion. It:
  • Takes user input
  • Decides which tools to call (via LLM)
  • Executes tools and collects results
  • Returns final answer to user

Main Components:
  - Agent.__init__()  → Sets up the agent
  - Agent.input()     → Main entry point for user requests
  - ToolFactory       → Auto-generates tool schemas from Python functions
  - EventHooks        → Trigger custom code at key moments


🔄 LIFECYCLE - What Happens When You Call agent.input("task")
──────────────────────────────────────────────────────────────

STEP 1: Initialization (happens once)
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  agent = Agent(                                              │
│      name="my-agent",                                        │
│      tools=[search_web, calculate],                          │
│      model="gpt-4"                                           │
│  )                                                           │
│                                                              │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ├─→ [1.1] Load system prompt
                        │         from "{name}.md" file
                        │
                        ├─→ [1.2] Auto-generate tool schemas
                        │         ToolFactory reads function signatures
                        │         Creates OpenAI-compatible JSON schemas
                        │
                        └─→ [1.3] Initialize event hooks
                                  (optional: after_user_input, before_tools, etc.)


STEP 2: User Input Processing
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  result = agent.input("Search for Python news")             │
│                                                              │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ├─→ [2.1] 🪝 Trigger: after_user_input hook
                        │         You can modify/log the input here
                        │
                        ├─→ [2.2] 📤 Call LLM with:
                        │         - System prompt
                        │         - User message
                        │         - Available tools (JSON schemas)
                        │
                        └─→ [2.3] 📥 LLM responds with tool calls
                                  Example: [{"name": "search_web",
                                            "args": {"query": "Python news"}}]


STEP 3: Tool Execution Loop (if LLM requested tools)
┌──────────────────────────────────────────────────────────────┐
│  for tool_call in llm_response.tool_calls:                   │
│                                                              │
│    [3.1] 🪝 Trigger: before_each_tool hook                   │
│                                                              │
│    [3.2] 🔧 Execute the tool function                        │
│          search_web(query="Python news")                     │
│          ↓                                                   │
│          Returns: [{"title": "...", "url": "..."}]           │
│                                                              │
│    [3.3] 🪝 Trigger: after_each_tool hook                    │
│          You can modify/cache the result here                │
│                                                              │
│    [3.4] 📝 Collect result                                   │
│          results.append(tool_result)                         │
│                                                              │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       └─→ Loop continues for all tool calls


STEP 4: Send Results Back to LLM
┌──────────────────────────────────────────────────────────────┐
│  [4.1] 📤 Send tool results to LLM                           │
│        LLM now knows: search_web returned articles           │
│                                                              │
│  [4.2] 📥 LLM generates final answer                         │
│        "Here are the latest Python news: ..."                │
│                                                              │
│  [4.3] 💾 Save to eval logs (.co/evals/)                     │
│        Full conversation saved for replay/debugging          │
│                                                              │
│  [4.4] ✅ Return to user                                     │
│        return final_answer                                   │
└──────────────────────────────────────────────────────────────┘


📊 VISUAL FLOW - Simplified
────────────────────────────

    User
     │
     │ "Search for Python news"
     ↓
  ┌─────────────────┐
  │  agent.input()  │
  └────────┬────────┘
           │
           ├──→ 🪝 after_user_input hook
           │
           ├──→ 📤 LLM: "What should I do?"
           │
           ├──→ 📥 LLM: "Call search_web(query='Python news')"
           │
           ├──→ 🔧 Execute: search_web()
           │         │
           │         └──→ Returns: [articles...]
           │
           ├──→ 📤 LLM: "Here are the results"
           │
           ├──→ 📥 LLM: "Here are the latest Python news..."
           │
           └──→ ✅ Return answer to user


🔍 KEY CONCEPTS
────────────────
1. Tools are just Python functions with type hints
   def search_web(query: str) -> list[dict]:
       ...

2. ToolFactory auto-generates schemas - no manual config needed

3. Event hooks let you inject custom logic at any step:
   - after_user_input: Modify/log user requests
   - before_tools: Inspect planned tool calls
   - after_each_tool: Cache/modify tool results
   - after_tools: Process all results together

4. Everything is logged to .co/evals/ for debugging

5. The agent can make MULTIPLE rounds of tool calls
   (LLM → tools → LLM → tools → ... → final answer)


📦 DEPENDENCIES
────────────────
External:
  • openai / anthropic / google.generativeai - For LLM calls
  • pydantic - For type validation (in ToolFactory)

Internal:
  • tool_factory.py - Generates OpenAI tool schemas
  • event_hooks.py - Manages hook system
  • logger.py - Saves eval logs

Key Files:
  • agent.py - Main Agent class (YOU ARE HERE)
  • tool_factory.py - Auto-schema generation
  • {agent_name}.md - System prompt file
  • .co/evals/ - Saved conversation logs
```

## Output Format

Creates a `.diagram.txt` file in the same directory:
- `agent.py` → `agent.diagram.txt`
- `src/tools/` → `src/tools/module.diagram.txt`

The diagram always includes:
1. **Header**: File name and purpose
2. **Overview**: What this code does in plain English
3. **Lifecycle**: Numbered steps showing execution flow
4. **Visual Flow**: ASCII diagram of the process
5. **Key Concepts**: Important patterns and gotchas
6. **Dependencies**: What it imports and uses

## Diagram Style - Easy to Read

### Box Style for Components
```
┌─────────────────┐
│  Function Name  │  ← Clear labels
└────────┬────────┘
         │
         ├─→ Step 1: What happens
         ├─→ Step 2: What happens next
         └─→ Step 3: Final result
```

### Arrows for Flow
```
User Input
    │
    ↓              ← Simple vertical flow
Process
    │
    ↓
Output
```

### Numbered Steps for Clarity
```
[1.1] First substep
[1.2] Second substep
[2.1] Next major step
```

### Icons for Quick Recognition
```
📋 Overview section
🔄 Lifecycle/flow section
🔍 Key concepts section
📦 Dependencies section
🪝 Event hook
📤 Sending data
📥 Receiving data
🔧 Tool execution
💾 Saving data
✅ Success/completion
```

## When to Use This Skill

### ✅ Perfect For:
- **Reading unfamiliar code** - Get oriented quickly
- **Before modifying code** - Understand what you're changing
- **Code review** - Visualize what the PR actually does
- **Onboarding** - Help new team members understand the codebase
- **Debugging** - Trace where things go wrong
- **Documentation** - Create visual explanations

### 🎯 Best Used On:
- Core files (agent.py, server.py, main.py)
- Complex logic (state machines, workflows)
- API endpoints and handlers
- Class hierarchies
- Module interactions

## Tips for Best Results

### 1. **Be Specific**
```bash
# ❌ Too vague
/diagram src/

# ✅ Specific
/diagram src/agent.py
/diagram src/agent.py "focus on tool execution"
```

### 2. **Focus on What Matters**
The diagram shows:
- ✅ Core lifecycle (initialization → processing → cleanup)
- ✅ Main execution path (the "happy path")
- ✅ Key decision points (if/else, loops)
- ✅ Important state changes
- ❌ Every single line of code
- ❌ Minor helper functions (unless requested)

### 3. **Use for Learning, Not Replacing Code Reading**
The diagram helps you understand the *flow* and *architecture*.
You still need to read the actual code for details.

### 4. **Iterate**
```bash
# First pass - overview
/diagram src/agent.py

# Second pass - specific area
/diagram src/agent.py "explain how event hooks work"

# Third pass - another module
/diagram src/tool_factory.py
```

## How It Works (Meta)

1. **Read** - The skill reads the code file(s) you specify
2. **Analyze** - Identifies key functions, classes, and flows
3. **Structure** - Organizes into: Overview → Lifecycle → Concepts → Dependencies
4. **Visualize** - Creates ASCII diagrams with boxes and arrows
5. **Explain** - Adds plain English explanations at each step
6. **Save** - Writes to `.diagram.txt` file

## Example Use Cases

### Use Case 1: Understanding a New Feature
```bash
# You're assigned to fix a bug in tool execution
/diagram src/agent.py "tool execution flow"

# Read the diagram to understand:
# - Where tools are called
# - What hooks are involved
# - How errors are handled
# - Where to add your fix
```

### Use Case 2: Code Review
```bash
# Reviewer wants to understand a PR that modified agent.py
/diagram src/agent.py

# Compare diagram with actual changes:
# - Does the flow still make sense?
# - Are there new edge cases?
# - Is error handling complete?
```

### Use Case 3: Architectural Overview
```bash
# New team member joining
/diagram src/

# They get a clear picture of:
# - How the system is organized
# - What each module does
# - How modules interact
# - Where to start reading code
```
