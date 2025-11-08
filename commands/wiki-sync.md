---
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, TodoWrite, WebSearch
argument-hint: [focus-recent|full-sync|new-topics]
description: AI-driven wiki content synthesis from docs/ with SEO optimization (comprehension-based, not copy-paste)
---

# Wiki Content Synthesis and SEO Optimization

## Philosophy

**This is NOT a copy-paste tool.** This command reads and comprehends documentation, then creates better SEO-optimized wiki content based on understanding.

**Process:**
1. Read and understand ALL documentation
2. Identify recent changes (git log analysis)
3. Research SEO keywords and user intent
4. Synthesize new wiki content (better than original docs)
5. Add SEO structure, examples, and cross-links
6. Commit with clear documentation of changes

**Wiki Architecture:**
- Main repo: `connectonion/`
- Wiki repo (nested): `connectonion/wiki/` (separate Git repo)
- Wiki URL: https://github.com/wu-changxing/connectonion/wiki
- Docs site: https://docs.connectonion.com (canonical technical reference)

## Step 1: Discover Recent Changes

### Find recently updated documentation
Use git log to identify fresh content that needs wiki coverage:

```bash
# Last 4 weeks of changes
git log --since="4 weeks ago" --name-only --pretty=format:"%h %s" -- docs/*.md

# Group by file to see most active docs
git log --since="4 weeks ago" --name-only --pretty=format:"" -- docs/*.md | sort | uniq -c | sort -rn
```

**Create TodoWrite list** of recently changed docs to prioritize:
```
High Priority (changed in last 4 weeks):
- docs/agent.md - [commit message]
- docs/models.md - [commit message]
- docs/auto_debug.md - [commit message]

Medium Priority (changed 4-8 weeks ago):
...
```

## Step 2: Comprehensive Reading Phase

**Read ALL documentation to build understanding:**

### A. Core Concepts
Read and comprehend:
- `docs/agent.md` - Agent orchestration, tool calling
- `docs/getting-started.md` - Onboarding flow
- `docs/concepts.md` - Framework philosophy
- `docs/trust.md` - Security model
- `docs/api.md` - API reference

### B. Features
- `docs/auto_debug.md` - Interactive debugging
- `docs/debug.md` - Debugging approaches
- `docs/cli.md` - Command-line interface
- `docs/auth.md` - Authentication system
- `docs/models.md` - LLM provider support
- `docs/templates.md` - Project templates

### C. Examples
- `docs/examples.md` - Code examples
- `docs/get_emails.md` - Gmail integration
- All examples in `docs/`

### D. Build Mental Model
After reading, understand:
- **What's new?** Recent features, API changes
- **What's confusing?** Gaps that wiki should clarify
- **What's missing?** Topics in docs not covered in wiki
- **User pain points?** Common questions, errors

**Use Grep to cross-reference** related concepts across docs:
```bash
grep -r "auto_debug" docs/ --include="*.md"
grep -r "trust" docs/ --include="*.md"
grep -r "agent.input" docs/ --include="*.md"
```

## Step 3: SEO Keyword Research

For priority topics (from Step 1), research what users are searching:

### A. Search Intent Analysis
Use WebSearch to find:
```
"python ai agent tutorial"
"how to debug ai agent python"
"connectonion vs langchain"
"openai function calling python"
"ai agent tools python"
"[recent feature from docs] tutorial"
```

### B. Extract Insights
From search results, identify:
- **Common questions** people ask (forums, Reddit, Stack Overflow)
- **Terminology** users actually use (may differ from docs)
- **Related searches** (Google "People also ask")
- **Long-tail keywords** (3-5 words, lower competition)
- **Problem-based searches** ("agent not calling tools", "api error")

### C. Create Keyword Map
For each wiki page to create:
```
Topic: Agent Basics
Primary keyword: "python ai agent tutorial" (10K/month)
Secondary keywords:
- "build ai agent python" (2K/month)
- "openai agent tutorial" (1K/month)
- "ai agent framework python" (500/month)

Search intent: Beginners want step-by-step guide to create first agent
Content angle: Beginner-friendly tutorial with working code
```

## Step 4: Inventory Existing Wiki

### A. List current wiki pages
```bash
cd wiki/
find . -name "*.md" -type f | sort
```

Current structure:
- Home.md
- Quick-Start.md
- Tutorials/ (3 pages)
- How-To/ (3 pages)
- Examples/ (2 pages)
- FAQ.md
- Troubleshooting.md
- _Sidebar.md

### B. Identify Gaps
Compare docs topics vs wiki coverage:

**Covered in wiki:**
- ✅ Quick start
- ✅ Building first agent
- ✅ Auto-debug usage
- ✅ Custom tools
- ✅ Email agent example
- ✅ Web scraping example
- ✅ Production deployment

**Missing from wiki** (based on docs reading):
- ❌ Agent core concepts (docs/agent.md)
- ❌ Trust system guide (docs/trust.md)
- ❌ Authentication setup (docs/auth.md)
- ❌ CLI commands reference (docs/cli.md)
- ❌ Multi-model support (docs/models.md)
- ❌ Template usage (docs/templates.md)
- ❌ Logging and monitoring (docs/log.md)

### C. Identify Outdated Content
Check if wiki pages need updates based on recent docs changes:
- Read existing wiki page
- Compare with understanding from docs
- Note discrepancies, missing info

## Step 5: Content Synthesis (AI-Driven Creation)

For each page to create/update, **do NOT copy docs**. Instead:

### A. Synthesize from Understanding
Based on your comprehension of docs:
1. **Explain** concept in beginner-friendly language
2. **Add context** that docs assume
3. **Include examples** that show real usage
4. **Answer questions** that docs don't address
5. **Connect concepts** to related topics

### B. Apply SEO Template
```markdown
# [Topic] - [Primary Keyword] | ConnectOnion

**[150-160 char value proposition with primary keyword]**

## What You'll Learn
- [Outcome 1 with keyword]
- [Outcome 2 with keyword]
- [Outcome 3 with keyword]

## Quick Links
- [Jump to code examples](#code-examples)
- [Jump to common issues](#common-issues)
- [Jump to next steps](#next-steps)

## [H2 Section - Use Question Format]

### [H3 Subsection with Keyword]

[2-3 short paragraphs explaining concept]

**Key Points:**
- Bullet 1
- Bullet 2
- Bullet 3

### Code Example

```python
# Working, copy-pasteable code
# Show expected output as comments
```

**Expected Output:**
```
[Actual output when code runs]
```

## Common Issues (targets "problem" searches)

### Issue 1: [Error message people search for]
**Symptoms:** [What user sees]
**Cause:** [Why it happens]
**Solution:** [How to fix]

### Issue 2: [Another common problem]
...

## Real-World Example

[Complete working example with context]

## Next Steps

Now that you understand [topic], explore:
- [Related wiki page 1 with context]
- [Related wiki page 2 with context]
- [Related wiki page 3 with context]

---

**Related Pages:**
- [Cross-link 1]
- [Cross-link 2]
- [Cross-link 3]
```

### C. Content Guidelines

**Writing Style:**
- Beginner-friendly (simpler than docs)
- Short paragraphs (2-3 lines max)
- Active voice, second person ("you")
- Concrete examples, not abstract concepts
- Show code output, not just code

**SEO Requirements:**
- Title: Contains primary keyword
- First paragraph: Primary keyword + value prop (150-160 chars)
- Headings (H2/H3): Question format with keywords
- Code examples: At least 2 with output
- Internal links: 3-5 to other wiki pages
- External links: Link to docs site for deep dives
- Word count: 1000-2000 words
- FAQ section: Common questions with keywords

**Quality Checks:**
- Can a beginner understand this?
- Does it answer questions docs don't?
- Are examples copy-pasteable and tested?
- Does it link to next learning steps?
- Is it better than just reading docs?

## Step 6: Execution Strategy

### Mode: `focus-recent` (default)
Focus on recently changed docs first:

1. Work through TodoWrite list (from Step 1)
2. For each recent doc change:
   - Re-read the doc with changes
   - Understand what's new/different
   - Check if wiki needs update or new page
   - Synthesize improved content
   - Add SEO structure
3. Update `_Sidebar.md` if new pages added
4. Commit batch of related changes

### Mode: `full-sync`
Comprehensive update of entire wiki:

1. Read ALL docs (Step 2)
2. Review ALL wiki pages
3. Update outdated content
4. Fill all gaps (create missing pages)
5. Add cross-links throughout
6. Optimize all pages for SEO

### Mode: `new-topics`
Create new wiki pages for uncovered topics:

1. Identify gaps (Step 4.B)
2. Research keywords for each gap
3. Synthesize content for each
4. Create new pages with SEO structure
5. Add to navigation

## Step 7: Cross-Linking and Navigation

### A. Add Internal Links
For each page, add 3-5 contextual links:

**Bad linking:**
```markdown
See [Agent Basics](Tutorials/Agent-Basics).
```

**Good linking:**
```markdown
To understand how agents work under the hood, read the
[Agent Basics tutorial](Tutorials/Agent-Basics) which explains
the execution loop and tool calling process.
```

### B. Update _Sidebar.md
Add new pages to navigation with clear hierarchy:

```markdown
### Getting Started
- [Home](Home)
- [Quick Start](Quick-Start)

### Tutorials
- [Building Your First Agent](Tutorials/Building-Your-First-Agent)
- [Agent Core Concepts](Tutorials/Agent-Core-Concepts) ← NEW
- [Trust System](Tutorials/Trust-System-Guide) ← NEW
...
```

### C. Cross-Reference Strategy
Link pages bidirectionally:
- Basics → Advanced ("Next steps")
- Advanced → Basics ("Prerequisites")
- Related concepts → Each other
- Tutorials → Examples
- Examples → How-To guides

## Step 8: Quality Verification

Before creating each page, use TodoWrite checklist:

```
Page: wiki/Tutorials/Agent-Core-Concepts.md

Content Quality:
- [ ] Read docs/agent.md, docs/getting-started.md, docs/api.md
- [ ] Understood core concepts deeply
- [ ] Wrote in own words (not copy-paste)
- [ ] Added beginner context missing from docs
- [ ] Included 2+ working code examples
- [ ] Showed expected output
- [ ] More accessible than docs

SEO Quality:
- [ ] Title contains "python ai agent" keyword
- [ ] First paragraph is 150-160 chars with keyword
- [ ] 3-5 question-format headings with keywords
- [ ] Added FAQ section
- [ ] Included common errors section
- [ ] 3-5 internal links to other wiki pages
- [ ] Linked to docs.connectonion.com for deep dive
- [ ] 1000-2000 word count
- [ ] Short paragraphs, scannable

Technical Quality:
- [ ] Code examples are tested and work
- [ ] No broken links
- [ ] Consistent terminology
- [ ] Clear "Next Steps" section
- [ ] Proper markdown formatting
```

## Step 9: Commit Strategy

Commit related changes together:

```bash
cd wiki/
git status
git add Tutorials/Agent-Core-Concepts.md
git add Tutorials/Trust-System-Guide.md
git add _Sidebar.md

git commit -m "Add agent concepts and trust system tutorials

Based on recent docs updates to agent.md and trust.md.

Created:
- Tutorials/Agent-Core-Concepts.md (keyword: python ai agent tutorial)
- Tutorials/Trust-System-Guide.md (keyword: ai agent security)

SEO improvements:
- Added beginner-friendly explanations
- Included working code examples with output
- Added FAQ sections for common questions
- Cross-linked to existing tutorials
- Updated sidebar navigation

Target keywords: python ai agent, ai agent security, openai function calling
Estimated monthly searches: ~15K combined"

git push origin master
```

## Step 10: Summary Report

After sync, provide:

### A. Changes Made
```
Created (3 pages):
- Tutorials/Agent-Core-Concepts.md (1,847 words)
- Tutorials/Trust-System-Guide.md (1,523 words)
- Reference/CLI-Commands.md (1,201 words)

Updated (2 pages):
- How-To/Use-Auto-Debug.md (added new debugging modes from docs)
- Quick-Start.md (updated API key setup based on auth.md changes)
```

### B. SEO Impact
```
Primary Keywords Targeted:
- "python ai agent tutorial" (10K/month)
- "ai agent security" (2K/month)
- "connectonion cli" (500/month)

Total New Content: 4,571 words
Internal Links Added: 17
External Links to Docs Site: 5

Estimated Impact:
- 3 new long-tail keyword opportunities
- Better coverage of recent feature updates
- Improved beginner onboarding path
```

### C. Next Steps
```
Recommended for next sync:
1. Create guide for models.md changes (multi-provider support)
2. Update examples with new CLI workflow
3. Add troubleshooting page for auth issues
4. Create comparison guide (ConnectOnion vs alternatives)
```

## SEO Strategy Notes

**Wiki Role:** Discovery and onboarding (SEO focus)
- Target: Beginners searching for tutorials
- Keywords: How-to, tutorial, guide, example
- Content: Accessible, example-driven
- Links: Guide users to docs site for details

**Docs Site Role:** Comprehensive reference (canonical)
- Target: Users who found us, need full docs
- Keywords: API reference, specification
- Content: Complete, technical, authoritative
- Links: Deep technical content

**Synergy:**
- Wiki captures long-tail searches → drives discovery
- Wiki links to docs site → keeps users engaged
- Docs site has canonical technical content
- Both cross-reference each other

## Priority Topics (Based on Search Volume)

**High Priority** (create/optimize first):
1. Python AI agent tutorial (10K+/month)
2. How to debug AI agent (5K/month)
3. OpenAI function calling tutorial (3K/month)
4. AI agent examples (2K/month)
5. AI agent tools (2K/month)

**Medium Priority:**
1. Deploy AI agent production (1K/month)
2. AI agent security/trust (500/month)
3. Multi-agent systems (500/month)
4. Local AI models (300/month)

## Example Transformation

### Docs Content (Technical):
```
# Agent

The Agent class orchestrates LLM calls with tool execution.
It maintains conversation history and handles tool calling...
```

### Wiki Content (SEO + Beginner-Friendly):
```
# How AI Agents Work - Python Agent Tutorial | ConnectOnion

**Learn how AI agents combine language models with tools to complete
tasks autonomously - step-by-step tutorial with working code examples.**

## What You'll Learn
- How AI agents decide when to use tools
- The agent execution loop explained
- Building your first tool-using agent

## How AI Agents Work

AI agents are like smart assistants that can use tools. Instead of
just answering questions, they can take actions: search databases,
send emails, call APIs.

Here's the magic: the AI decides WHEN to use tools based on your request.

### Simple Example

```python
from connectonion import Agent

def search_database(query: str) -> str:
    """Search our product database"""
    return f"Found 10 products matching '{query}'"

agent = Agent("assistant", tools=[search_database])
agent.input("Find blue shirts")
```

**What happens:**
1. Agent reads your message: "Find blue shirts"
2. Agent thinks: "I need to search the database"
3. Agent calls: `search_database("blue shirts")`
4. Agent responds: "I found 10 blue shirts in our database..."

[Continue with more beginner-friendly explanation, examples, FAQs...]
```

## Remember

**This is synthesis, not copying:**
- Read docs to understand
- Research what users need
- Create better content based on knowledge
- Add SEO structure during creation
- Make it more accessible than docs

**Quality over quantity:**
- One great page > five mediocre pages
- Real understanding > surface copying
- User value > keyword stuffing
