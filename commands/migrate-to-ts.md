---
allowed-tools: Glob, Grep, Read, Edit, Write, TodoWrite, Bash
argument-hint: [feature-description-or-file:line]
description: Migrate one Python ConnectOnion feature to TypeScript version
---

# ConnectOnion Python to TypeScript Migration (Single Feature)

## Core Migration Principles

### 1. Less Code = Better Code
- Python 5 lines → TypeScript 5 lines
- Don't add code that wasn't there
- Simple function stays a simple function

### 2. Don't Make User Learn New Things
- Python used pattern X → TypeScript uses equivalent pattern X
- Don't introduce "better" patterns or concepts
- User already knows Python way, keep it the same
- If Python didn't need it, TypeScript doesn't need it

### 3. Let It Crash
- NO try-catch unless Python had try-except
- Errors are good - let them throw
- Don't hide problems with error handling

### 4. Read First, Code Later
- Read Python file
- Read related files
- Read TypeScript SDK examples
- Create todo list
- Then migrate

## Step 1: Read and Understand Context

### 1.1 Read the Python file
- Use Read tool to read the entire Python file
- Understand what it does overall
- Don't start migrating yet - just read

### 1.2 Find and read related files
Use Grep to find:
- Files that import this file: `grep -r "from.*import" --include="*.py"`
- Files this imports from
- Related examples or tests

Read ALL related files:
- Tool definitions
- Agent configurations
- Helper functions
- Example usage

### 1.3 Read TypeScript SDK patterns
Read these TypeScript files for reference:
- `connectonion-ts/src/core/agent.ts` - Agent API
- `connectonion-ts/examples/` - Examples
- Look for similar patterns to what you're migrating

### 1.4 Read documentation
If migrating a documented feature:
- Read Python docs
- Read TypeScript docs
- Note differences in API

## Step 2: Create Todo List

Use TodoWrite to create a plan:
```
1. Read [python-file] - pending
2. Read related files: [list] - pending
3. Read TypeScript examples - pending
4. Identify features to migrate: [list] - pending
5. Migrate feature: [specific-feature] - pending
6. Test migrated code - pending
```

DO NOT start migrating until all reading is done.

## Step 3: Identify ONE Feature to Migrate

### 3.1 List all features found
After reading, show user:
```
Found these features in [file]:
1. Tool function: search(query: str) -> str
2. Tool function: calculate(expr: str) -> float
3. Agent creation: Agent(name="assistant", tools=[...])
4. Main execution: main() function

Which ONE do you want to migrate first?
```

### 3.2 User selects one feature
Wait for user to pick

### 3.3 Mark in todo list
Update TodoWrite:
- Mark reading tasks as completed
- Set chosen feature as 'in_progress'

## Step 4: Simple Direct Migration

### 4.1 Extract ONLY the feature code
Don't grab extra code - just the ONE feature

### 4.2 Translate directly
Apply these simple rules:

**Syntax Changes:**
- `def function_name` → `function functionName`
- `snake_case` → `camelCase`
- `: str` → `: string`
- `: int` / `: float` → `: number`
- `: bool` → `: boolean`
- `f"text {var}"` → `` `text ${var}` ``
- `"""docstring"""` → `/** docstring */`
- `print()` → `console.log()`

**Agent Creation:**
- `Agent(name="x", tools=[...])` → `new Agent({name: "x", tools: [...]})`
- `system_prompt` → `systemPrompt`
- `max_iterations` → `maxIterations`

**Async:**
- `agent.input()` needs `await` in TypeScript
- Make parent function `async`

**IMPORTANT - What NOT to do:**
- ❌ NEVER add try-catch if Python didn't have try-except
- ❌ NEVER add .catch() if Python didn't handle errors
- ❌ Don't add type interfaces for simple objects
- ❌ Don't refactor or "improve" the code
- ❌ Don't add error handling that wasn't there
- ❌ Don't create helper functions that didn't exist
- ❌ Don't add validation that wasn't in Python
- ❌ Just let it crash - errors are good information

## Step 5: Show Side-by-Side Comparison

Display:
```
=== Python (Original) ===
[original Python code]

=== TypeScript (Migrated) ===
[migrated TypeScript code]

Changes made:
- [list specific transformations]

NOT changed (keeping original behavior):
- [list what was kept the same]
```

Ask user: "Does this look correct?"

## Step 6: Save the Migrated Code

### 6.1 Determine output location
Ask user:
1. Create new file: `[name].ts`
2. Append to existing file
3. Show me the full file content first

### 6.2 Write minimal file
If creating new file:
```typescript
/**
 * Migrated from: [source-file]
 */

import { Agent } from 'connectonion-ts';

[migrated code]

// Example usage:
async function main() {
    [if applicable]
}

// Let it crash - no .catch()
// main();
```

Keep it minimal - no extra boilerplate.

### 6.3 Update todo list
Mark feature as completed

## Step 7: Setup Environment for Testing

### 7.1 Check for .env file
Check if `.env` file exists in the output directory

### 7.2 Copy .env from connectonion example
If no .env exists:
```bash
cp /Users/changxing/project/OnCourse/platform/connectonion/examples/minimal-agent/.env .
```

Or read the .env and create one in the current directory:
- Read the source .env file
- Write it to the output directory
- This ensures API keys are available for testing

### 7.3 Inform user about .env
Show:
```
✅ Environment setup:
- Copied .env from connectonion/examples/minimal-agent/
- API keys available for testing
- Location: [path-to-.env]
```

## Step 8: Create Test File

### 8.1 Create simple test file
For the migrated feature, create `[feature-name].test.ts`:

**For a tool function:**
```typescript
/**
 * Test for migrated [feature-name]
 */

import { [functionName] } from './[feature-file]';

async function test() {
    console.log('Testing [functionName]...');

    // Test case 1
    const result1 = [functionName]([test-input]);
    console.log('✓ Test 1:', result1);

    // Test case 2 (if applicable)
    const result2 = [functionName]([test-input-2]);
    console.log('✓ Test 2:', result2);

    console.log('✅ All tests passed');
}

// Let it crash - no .catch()
test();
```

**For an agent:**
```typescript
/**
 * Test for migrated agent
 */

import { Agent } from 'connectonion-ts';
import * as dotenv from 'dotenv';

dotenv.config();

async function test() {
    console.log('Testing agent...');

    const agent = new Agent({
        [agent-config]
    });

    // Test case 1
    console.log('\n=== Test 1: [description] ===');
    const result1 = await agent.input('[test-prompt-1]');
    console.log('Result:', result1);

    // Test case 2 (if applicable)
    console.log('\n=== Test 2: [description] ===');
    const result2 = await agent.input('[test-prompt-2]');
    console.log('Result:', result2);

    console.log('\n✅ All tests passed');
}

// Let it crash - no .catch()
test();
```

### 8.2 Keep tests simple
- Don't add test frameworks (no jest, no mocha)
- Just simple console.log checks
- If it runs without error, it passes
- Match the test style from Python if tests existed

### 8.3 Update todo list
Add test to todo:
- Run test: `npx tsx [feature-name].test.ts` - pending

## Step 9: Run the Test

### 9.1 Execute test file
Run the test:
```bash
npx tsx [feature-name].test.ts
```

### 9.2 Show results
Display test output:
```
Running test...
[output]

✅ Test passed
OR
✗ Test failed: [error]
```

### 9.3 If test fails
- Show the error
- Check if it's a simple fix (missing import, typo)
- Fix and rerun
- Don't over-engineer the fix - keep it simple

### 9.4 Update todo list
Mark test as completed

## Step 10: Next Feature

Ask: "Feature migrated and tested! What do you want to migrate next?"

Update TodoWrite with next item as 'in_progress'

## Migration Pattern Examples

### Example 1: Simple Tool (Keep It Simple)

**Python:**
```python
def search(query: str) -> str:
    """Search for information."""
    return f"Results for {query}"
```

**TypeScript (Correct - Simple):**
```typescript
function search(query: string): string {
    return `Results for ${query}`;
}
```

**TypeScript (WRONG - Over-engineered):**
```typescript
// ❌ Don't do this - adding unnecessary types
interface SearchResult {
    query: string;
    results: string;
}

class SearchService {
    search(query: string): SearchResult {
        try { // ❌ Unnecessary try-catch
            return {
                query,
                results: `Results for ${query}`
            };
        } catch (e) {
            return { query, results: '' };
        }
    }
}
```

### Example 2: Let It Crash

**Python:**
```python
def calculate(expr: str) -> float:
    return eval(expr)  # Will throw if invalid
```

**TypeScript (Correct - Let It Crash):**
```typescript
function calculate(expr: string): number {
    return eval(expr);  // Will throw if invalid - that's good
}
```

**TypeScript (WRONG - Over-engineered):**
```typescript
// ❌ Don't do this - adding error handling that wasn't there
function calculate(expr: string): number {
    try {
        const result = eval(expr);
        if (typeof result !== 'number') {
            throw new Error('Result is not a number');
        }
        return result;
    } catch (e) {
        console.error('Calculation failed:', e);
        return 0; // ❌ Hiding the error
    }
}
```

### Example 3: Direct Translation

**Python:**
```python
agent = Agent(
    name="assistant",
    tools=[search],
    model="gpt-4o-mini"
)
result = agent.input("Hello")
```

**TypeScript (Correct):**
```typescript
const agent = new Agent({
    name: "assistant",
    tools: [search],
    model: "gpt-4o-mini"
});
const result = await agent.input("Hello");
```

**TypeScript (WRONG - Over-engineered):**
```typescript
// ❌ Don't do this - adding abstraction
interface AgentConfig {
    name: string;
    tools: Tool[];
    model: string;
}

class AgentFactory {
    static createAgent(config: AgentConfig): Agent {
        try {
            const agent = new Agent(config);
            return agent;
        } catch (e) {
            throw new Error(`Failed to create agent: ${e}`);
        }
    }
}

const config: AgentConfig = {
    name: "assistant",
    tools: [search],
    model: "gpt-4o-mini"
};

const agent = AgentFactory.createAgent(config);
```

## Type Conversion Reference

| Python Type | TypeScript Type | Notes |
|-------------|-----------------|-------|
| `str` | `string` | Direct mapping |
| `int`, `float` | `number` | Both become number |
| `bool` | `boolean` | Direct mapping |
| `List[T]` | `T[]` | Keep it simple |
| `Dict[K,V]` | `Record<K,V>` | Or just `any` if complex |
| `Optional[T]` | `T \| undefined` | Usually optional params |
| `None` | `null` or `undefined` | Context dependent |
| `Any` | `any` | It's okay to use `any` |

## Checklist Before Writing Code

- [ ] Read the Python file completely
- [ ] Read all files it imports from
- [ ] Read TypeScript SDK for reference
- [ ] Created todo list with TodoWrite
- [ ] Identified ONE specific feature to migrate
- [ ] Understand what it does (not just syntax)
- [ ] Know where the output file should go
- [ ] Ready to do DIRECT translation (no improvements)

## Checklist After Writing Code

- [ ] TypeScript is same simplicity level as Python
- [ ] No try-catch added unless Python had it
- [ ] No new abstractions or patterns
- [ ] Types are simple (no complex interfaces for simple objects)
- [ ] Async/await added where needed
- [ ] User confirmed it looks correct
- [ ] .env file copied from connectonion/examples/simple-agent/
- [ ] Test file created
- [ ] Test ran successfully
- [ ] Todo list updated

## Red Flags (Stop and Ask User)

If you find yourself doing any of these, STOP:
- 🚩 Adding error handling that wasn't in Python
- 🚩 Creating interfaces or types for simple objects
- 🚩 Refactoring or "improving" the structure
- 🚩 Adding validation logic
- 🚩 Creating helper functions that didn't exist
- 🚩 Making the TypeScript more complex than Python
- 🚩 Adding comments explaining "better practices"

Ask user: "The Python code doesn't have [X]. Should I add it or keep it simple?"

## Philosophy

**Remember:**
- We're migrating, not improving
- Simple code is good code
- Errors are information - don't hide them
- If you're unsure about a type, use `any`
- 5 lines of Python = 5 lines of TypeScript
- When in doubt, keep it simpler

**Goal:**
Get Python code running in TypeScript with minimal changes.
Not to make it "better" or "more TypeScript-y".

## Success Criteria

One feature is successfully migrated when:
- ✅ Read all related files first
- ✅ Created and followed todo list
- ✅ TypeScript matches Python's simplicity
- ✅ No unnecessary error handling added
- ✅ No over-engineering or abstractions
- ✅ User confirmed it looks correct
- ✅ .env file available for testing
- ✅ Test file created and runs successfully
- ✅ Feature works as expected
- ✅ Ready for next feature migration
