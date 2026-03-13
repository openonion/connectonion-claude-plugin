---
allowed-tools: Read, Glob, Grep, Write
description: Analyze code and draw ASCII diagram to explain lifecycle and flow
argument-hint: <file-or-directory>
---

# Code Flow Diagram

Read code and create ASCII diagrams that explain the core lifecycle and how things work.

## Usage

```bash
# Analyze a file
/diagram src/agent.py

# Analyze with focus
/diagram src/agent.py "explain the tool execution flow"
```

## What You Get

Simple ASCII diagrams that show:
- **Lifecycle**: How objects are created → used → cleaned up
- **Flow**: Step-by-step execution path
- **Interactions**: How components talk to each other
- **Data flow**: How data transforms through the code

## Example Output

```
Agent Lifecycle
===============

1. Initialization
   ┌─────────────────┐
   │ Agent.__init__  │
   └────────┬────────┘
            │
            ├─→ Load system prompt from .md file
            ├─→ Auto-generate tool schemas
            └─→ Setup event hooks

2. Processing Input
   ┌──────────────┐
   │ agent.input()│
   └──────┬───────┘
          │
          ├─→ Trigger: after_user_input hook
          │
          ├─→ Call LLM with prompt + tools
          │
          ├─→ LLM returns tool calls
          │    │
          │    └─→ Loop: Execute each tool
          │         ├─→ Trigger: before_each_tool
          │         ├─→ Run tool function
          │         ├─→ Trigger: after_each_tool
          │         └─→ Collect results
          │
          ├─→ Send results back to LLM
          │
          └─→ Return final response

3. Tool Execution Detail

   User Input
      ↓
   "Search for Python news"
      ↓
   ┌────────────────────┐
   │  LLM decides:      │
   │  Call search_web() │
   └─────────┬──────────┘
             ↓
   ┌─────────────────────┐
   │ Execute tool:       │
   │ search_web("Python")│
   └─────────┬───────────┘
             ↓
   ┌──────────────────────┐
   │ Results: [articles]  │
   └─────────┬────────────┘
             ↓
   Back to LLM → Final Answer
```

## Output Format

Creates a `.diagram.txt` file with:
- **Overview**: High-level architecture
- **Lifecycle**: Step-by-step flow
- **Key Points**: Important notes about the code
- **Dependencies**: What it relies on

## When to Use

- **Understanding new code**: Before making changes
- **Code review**: Visualize what the code does
- **Documentation**: Explain complex flows
- **Debugging**: Trace execution paths

## Tips

- Focus on core lifecycle, not every detail
- Shows the "happy path" by default
- Add notes about error handling
- Explains WHY not just WHAT
