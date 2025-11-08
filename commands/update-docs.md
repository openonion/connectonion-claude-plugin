# Update Documentation Command

Update all documentation for a feature with deep understanding first.

## Usage
```bash
/update-docs <feature-name>
```

Example:
```bash
/update-docs auto_debug
```

## Workflow

### Step 1: Deep Understanding - Read Everything
**Goal: Understand WHY people use this feature, not just what it does**

Read in this order:
1. **Implementation code**:
   - Main feature files (e.g., `connectonion/auto_debug.py`, `connectonion/xray.py`)
   - Related files and dependencies
   - Test files to see real usage patterns

2. **Existing documentation**:
   - `docs/<feature-name>.md` - Current docs
   - Related docs that mention the feature
   - Code comments and docstrings

3. **Examples and demos**:
   - Example files in `simple-agent/` or `examples/`
   - Test files showing usage patterns
   - README sections

4. **User perspective**:
   - What problem does this solve?
   - What pain points does it address?
   - What are the "aha!" moments?
   - When would someone reach for this feature?
   - What alternatives exist and why is this better?

Take notes on:
- Key use cases
- Common patterns
- Edge cases
- Integration points
- User mental model

### Step 2: Draft Main Documentation (docs/)
**Create comprehensive reference documentation**

Edit `docs/<feature-name>.md`:
- Start with the problem/pain point
- Show simplest usage first (60-second success)
- Progressive disclosure of complexity
- Real-world examples, not abstract concepts
- Show actual output
- Include best practices
- Document edge cases
- Link to related features

Format:
```markdown
# Feature Name

One-sentence problem this solves.

## Quick Start (60 seconds)
[Minimal working example]

## Why Use This
[Problem/pain point it addresses]

## How It Works
[Core concepts]

## Complete Example
[Real-world usage]

## Best Practices
[Dos and don'ts]

## See Also
[Related features]
```

### Step 3: Update GitHub Wiki
**IMPORTANT: Wiki is a nested Git repository in `wiki/` folder**

The wiki is a **completely separate Git repository** inside the `wiki/` directory:
- Main repo ignores `wiki/` (in `.gitignore`)
- Wiki has its own `.git/` directory
- Wiki pushes to its own remote
- Must `cd wiki/` and commit separately

**Verify nested repo structure:**
```bash
# Check that wiki is ignored by main repo
git check-ignore -v wiki
# Should output: .gitignore:110:wiki/  wiki

# Verify wiki has its own git
ls -la wiki/.git
# Should show wiki's independent .git directory
```

**Navigate to wiki and check status:**
```bash
cd wiki/
git status
git remote -v  # Should show: https://github.com/openonion/connectonion.git
```

**Create/update wiki pages:**

Create how-to guide:
- File: `How-To-Use-<Feature>.md`
- Focus: Practical step-by-step guide

Create tutorial if complex:
- File: `Tutorials-<Feature>-Guide.md`
- Focus: Learning journey with explanations

Update sidebar:
- File: `_Sidebar.md`
- Add links to new pages

**Commit to wiki repo (separate from main repo!):**
```bash
git add .
git commit -m "Add <feature-name> documentation"
git push origin master
cd ..  # Return to main repo
```

Wiki content should:
- Be more tutorial-focused than docs/
- Show real problems users face
- Include troubleshooting
- Have lots of examples
- Be discoverable via Google search

### Step 4: Update Docs Site Navigation and Structure
**IMPORTANT: Docs site is a nested Git repository in `docs-site/` folder**

The docs-site is a **completely separate PRIVATE Git repository** inside the `docs-site/` directory:
- Main repo ignores `docs-site/` (in `.gitignore`)
- Docs-site has its own `.git/` directory
- Docs-site pushes to its own remote (private repo)
- Must `cd docs-site/` and commit separately

**Verify nested repo structure:**
```bash
# Check that docs-site is ignored by main repo
git check-ignore -v docs-site
# Should output: .gitignore:113:docs-site/  docs-site

# Verify docs-site has its own git
ls -la docs-site/.git
# Should show docs-site's independent .git directory
```

**Navigate to docs-site and check status:**
```bash
cd docs-site/
git status
git remote -v  # Should show: https://github.com/wu-changxing/connectonion-docs-site.git (private)
```

**Update navigation and structure:**

1. Update navigation (`lib/navigation.ts`):
```typescript
{
  title: 'Feature Name',
  href: '/feature-name',
  icon: IconName,
  section: 'Section Name',
  difficulty: 'Essential', // or 'Beginner', 'Intermediate'
  keywords: ['keyword1', 'keyword2', 'usage', 'pattern'],
  prev: { href: '/previous-page', title: 'Previous' },
  next: { href: '/next-page', title: 'Next' }
}
```

2. Check if page exists: `app/<feature-name>/page.tsx`
   - If not, create using existing page as template
   - If yes, plan updates

**Important:** Stay in `docs-site/` directory for next step (Step 5)

### Step 5: Refine Docs Site Page
**Create/refine the web page for best user experience**

**You should already be in `docs-site/` directory from Step 4**

Create or update `app/<feature-name>/page.tsx`:

Key principles:
- **Single column**: Easy to read on mobile
- **Copy button**: Let users copy all content as markdown
- **Progressive disclosure**: Simple → Advanced
- **Real output**: Show what actually happens
- **Scannable**: Bullet points, short sections
- **Code first**: Show working code immediately

Structure:
1. **Hero section**: Problem + 60-second solution
2. **Quick start**: Minimal working code
3. **Key features**: What you can do
4. **Complete examples**: Real-world usage
5. **Best practices**: Tips and gotchas
6. **See also**: Related features

Use components:
- `<CommandBlock>` for terminal commands
- `<CodeBlock>` for code examples
- Proper syntax highlighting
- Responsive design

**Commit to docs-site repo (still in docs-site/ directory!):**
```bash
# You should be in docs-site/ directory
git add app/ lib/
git commit -m "Add <feature-name> documentation"
git push origin main
cd ..  # Return to main repo
```

### Step 6: Update README.md and Quickstart
**Surface feature in main entry points**

Update `README.md`:
- Add to "What Makes ConnectOnion Special" section
- Add dedicated section with example
- Keep it concise (README shouldn't be too long)

Update `docs/quickstart.md`:
- Add practical example after basic setup
- Show when to use this feature
- Link to full documentation

### Step 7: Update PyPI Description (if main feature)
If this is a core feature, update `setup.py`:
- Mention in `long_description`
- Keep it brief
- Focus on user benefit

### Step 8: Update CLI Embedded Documentation
**IMPORTANT: After adding to website, update the embedded docs**

Update `connectonion/cli/docs/co-vibecoding-principles-docs-contexts-all-in-one.md`:
- This is the all-in-one docs file included with `co create` projects
- Add the feature documentation from the website
- Keep format consistent with existing content
- Include practical examples
- This helps users who drag docs to Cursor/Claude

Why this matters:
- Users can access docs offline
- Vibe coding: drag file into AI coding tools
- Self-contained project documentation

### Step 9: Verification Checklist
Before completing, verify:

**Understanding & Content:**
- [ ] Deeply understand WHY users need this
- [ ] Main docs (`docs/`) are comprehensive
- [ ] All code examples tested and work
- [ ] Links between docs are correct

**GitHub Wiki (Nested Repo):**
- [ ] GitHub wiki has how-to guide
- [ ] Wiki sidebar (_Sidebar.md) updated
- [ ] **COMMITTED to wiki repo** (`cd wiki/` → commit → push)
- [ ] Verify: `cd wiki && git log -1` shows your commit

**Docs Site (Nested Repo):**
- [ ] Docs site navigation updated
- [ ] Docs site page exists and looks good
- [ ] Mobile-friendly (docs-site)
- [ ] **COMMITTED to docs-site repo** (`cd docs-site/` → commit → push)
- [ ] Verify: `cd docs-site && git log -1` shows your commit

**Main Repo:**
- [ ] README mentions feature (if main)
- [ ] Quickstart has practical example
- [ ] PyPI description updated (if core feature)
- [ ] CLI embedded docs updated (`co-vibecoding-principles-docs-contexts-all-in-one.md`)
- [ ] **COMMITTED to main repo** (commit → push)
- [ ] Verify: `git log -1` shows your commit

**Architecture Verification:**
- [ ] Verify nested repos are ignored: `git check-ignore -v wiki docs-site`
- [ ] Verify no cross-contamination: `git ls-files | grep -E "^wiki/|^docs-site/"` (should be empty)

### Step 10: Summary
Provide summary of changes:
```
✅ Updated documentation for <feature-name>

Understanding gathered from:
- [List files read and key insights]

📚 GitHub Wiki (Nested Repo):
- Created/Updated: wiki/How-To-Use-<Feature>.md
- Updated: wiki/_Sidebar.md
- Commit: <commit-hash>
- Remote: https://github.com/openonion/connectonion.git (wiki)
- Status: ✅ Pushed to origin/master

🌐 Docs Site (Nested Repo - Private):
- Updated: docs-site/lib/navigation.ts
- Created/Updated: docs-site/app/<feature-name>/page.tsx
- Commit: <commit-hash>
- Remote: https://github.com/wu-changxing/connectonion-docs-site.git
- Status: ✅ Pushed to origin/main

📦 Main Repo:
- Updated: README.md
- Updated: docs/quickstart.md
- Updated: setup.py (if core feature)
- Updated: connectonion/cli/docs/co-vibecoding-principles-docs-contexts-all-in-one.md
- Commit: <commit-hash>
- Remote: https://github.com/openonion/connectonion.git
- Status: ✅ Pushed to origin/main

Architecture Verified:
- ✅ Wiki ignored by main repo
- ✅ Docs-site ignored by main repo
- ✅ No cross-contamination

Next steps:
- Test all examples
- Get feedback from users
- Monitor search ranking
```

## Example: auto_debug

### Step 1: Understanding
Read:
- `connectonion/agent.py` - `.auto_debug()` method
- `connectonion/interactive_debugger.py` - Main implementation
- `connectonion/xray.py` - `@xray` decorator
- `connectonion/debugger_ui.py` - UI components
- `simple-agent/agent_debug.py` - Real usage
- `docs/auto_debug.md` - Current docs

Key insights:
- Problem: Can't see why agents make decisions
- Solution: Pause at `@xray` tools, inspect state
- Why better: Like code debuggers but for AI agents
- Use cases: Understanding behavior, testing edge cases, prompt engineering

### Step 2-7: Update all docs following workflow above

## Notes

### Critical: Nested Repository Architecture

**Wiki and docs-site are SEPARATE Git repositories:**

```
connectonion/                    # Main repo
├── .git/                        # Main repo Git
├── .gitignore                   # Ignores: wiki/, docs-site/
├── connectonion/
├── tests/
├── wiki/                        # ← Nested repo (IGNORED by main)
│   ├── .git/                    # ← Independent git repo
│   └── *.md                     # Wiki pages
└── docs-site/                   # ← Nested repo (IGNORED by main)
    ├── .git/                    # ← Independent git repo (PRIVATE)
    └── app/                     # Docs pages
```

**Workflow:**
1. Make changes in `wiki/` → `cd wiki/` → commit → push → `cd ..`
2. Make changes in `docs-site/` → `cd docs-site/` → commit → push → `cd ..`
3. Make changes in main repo → commit → push (as normal)

**Verify architecture:**
```bash
# These should show both are ignored
git check-ignore -v wiki docs-site

# These should show independent .git directories
ls -d wiki/.git docs-site/.git
```

**Never remove from main .gitignore:**
- `wiki/` (line 110)
- `docs-site/` (line 113)

### Documentation Best Practices

- **Test everything**: Run every code example
- **User perspective**: Write for people with the problem, not people who know the solution
- **Progressive disclosure**: Simple first, advanced later
- **Real output**: Show what actually happens, not what you promise
