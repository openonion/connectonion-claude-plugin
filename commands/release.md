---
allowed-tools: Bash, Read, Edit, TodoWrite, WebSearch, Grep, Glob
argument-hint: [patch|minor|major|auto]
description: Automate version release - update version, build, publish to PyPI, create GitHub release, and update docs
---

# ConnectOnion Release Automation

## Purpose

Automates the complete release workflow including:
1. Version bumping (following VERSIONING.md rules)
2. Git tagging and pushing
3. PyPI package publishing
4. GitHub release creation with notes
5. Documentation updates
6. Community announcements

## Step 1: Determine Version Bump

### Read Current Version
```bash
# Check current version
grep "__version__" connectonion/__init__.py
```

### Calculate Next Version
Based on VERSIONING.md rules:
- **PATCH (0.2.X)**: Bug fixes, docs, refactoring, tests
- **MINOR (0.X.0)**: New features OR when PATCH reaches 10
- **MAJOR (X.0.0)**: Breaking changes OR when MINOR reaches 10

**Decision Logic:**
```
If argument is provided:
  - "patch" → increment PATCH
  - "minor" → increment MINOR (reset PATCH to 0)
  - "major" → increment MAJOR (reset MINOR and PATCH to 0)
  - "auto" → analyze git changes since last tag

If no argument:
  - Show recent commits since last tag
  - Ask user which type of release
  - Use TodoWrite to track decision
```

### Analyze Changes (for auto mode)
```bash
# Get last tag
git describe --tags --abbrev=0

# Show commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Search for keywords
git log $(git describe --tags --abbrev=0)..HEAD --oneline | grep -i "break\|feat\|fix\|docs\|refactor"
```

**Create TodoWrite list:**
```
Version Decision:
- Current: 0.2.1
- Proposed: 0.2.2 (PATCH)
- Reason: [based on commits analysis]
- Commits analyzed: 5
  - 3 bug fixes
  - 2 documentation updates
```

## Step 2: Update Version Files

### Files to Update
1. `/connectonion/__init__.py` - `__version__` variable
2. `/setup.py` - `version` parameter
3. `/VERSIONING.md` - Current version section
4. `/docs-site/app/page.tsx` - Version badge (if exists)

**Use Edit tool to update each file:**
```python
# Example: Update __init__.py
old: __version__ = "0.2.1"
new: __version__ = "0.2.2"
```

## Step 3: Generate Release Notes

### Collect Changes
```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s (%h)" --reverse

# Categorize by conventional commit types
git log $(git describe --tags --abbrev=0)..HEAD --oneline | awk '{
  if ($0 ~ /^[a-f0-9]+ (feat|feature):/) print "### ✨ Features\n- " substr($0, index($0, ":")+2)
  else if ($0 ~ /^[a-f0-9]+ fix:/) print "### 🐛 Bug Fixes\n- " substr($0, index($0, ":")+2)
  else if ($0 ~ /^[a-f0-9]+ docs:/) print "### 📚 Documentation\n- " substr($0, index($0, ":")+2)
  else if ($0 ~ /^[a-f0-9]+ refactor:/) print "### ♻️ Refactoring\n- " substr($0, index($0, ":")+2)
  else print "### 🔧 Other Changes\n- " substr($0, index($0, " ")+1)
}'
```

### Generate Release Notes Template
Create a structured release notes file:

```markdown
# Release v{VERSION}

## Highlights

[Summarize the most important changes in 2-3 sentences]

## What's Changed

### ✨ Features
- Feature 1 description
- Feature 2 description

### 🐛 Bug Fixes
- Fix 1 description
- Fix 2 description

### 📚 Documentation
- Doc improvement 1
- Doc improvement 2

### ♻️ Refactoring
- Refactor 1 description

## Installation

```bash
pip install connectonion=={VERSION}
```

## Breaking Changes

[List any breaking changes, or write "None"]

## Migration Guide

[If there are breaking changes, provide migration steps]

## Contributors

Thanks to all contributors! 🎉

**Full Changelog**: https://github.com/wu-changxing/connectonion/compare/v{PREVIOUS_VERSION}...v{VERSION}
```

## Step 4: Commit and Tag

### Commit Version Changes
```bash
git add connectonion/__init__.py setup.py VERSIONING.md

git commit -m "$(cat <<'EOF'
Release v{VERSION}: {SUMMARY}

{DETAILED_CHANGES}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Create Git Tag
```bash
# Annotated tag with release notes
git tag -a v{VERSION} -m "$(cat <<'EOF'
Release v{VERSION}

{RELEASE_NOTES}
EOF
)"
```

### Push to GitHub
```bash
git push origin main
git push origin v{VERSION}
```

**Use TodoWrite to track:**
```
Release Progress:
- [x] Version files updated
- [x] Release notes generated
- [x] Changes committed
- [x] Git tag created
- [x] Pushed to GitHub
- [ ] Build package
- [ ] Upload to PyPI
- [ ] Create GitHub release
```

## Step 5: Build and Publish Package

### Clean Previous Builds
```bash
rm -rf dist/ build/ *.egg-info
```

### Build Package
```bash
python setup.py sdist bdist_wheel
```

### Verify Build
```bash
ls -lh dist/
# Should show:
# connectonion-{VERSION}-py3-none-any.whl
# connectonion-{VERSION}.tar.gz
```

### Upload to PyPI
```bash
twine upload dist/connectonion-{VERSION}*
```

**Verify Upload:**
```bash
# Check PyPI page
curl -s https://pypi.org/pypi/connectonion/{VERSION}/json | jq -r '.info.version'
```

## Step 6: Create GitHub Release

### Using GitHub CLI
```bash
# Create release with notes from file
gh release create v{VERSION} \
  --title "Release v{VERSION}" \
  --notes-file /tmp/release-notes-{VERSION}.md \
  dist/connectonion-{VERSION}-py3-none-any.whl \
  dist/connectonion-{VERSION}.tar.gz
```

### Verify Release
```bash
gh release view v{VERSION}
```

## Step 7: Update Documentation Site

### Update Version Badge (if exists)
Check if docs site has version badge:
```bash
# Search for version references in docs site
grep -r "0\.2\." docs-site/ --include="*.tsx" --include="*.md"
```

If found, update using Edit tool.

### Rebuild Docs Site (if needed)
```bash
cd docs-site
npm run build
# Deploy if not auto-deployed
```

## Step 8: Create Community Announcement

### GitHub Discussion (Using GraphQL API)

**Why GraphQL?** GitHub Discussions only work via GraphQL API, not REST. The `gh` CLI doesn't have native discussion commands, so we use `gh api graphql`.

#### Step 8a: Get Repository ID (GraphQL Node ID)
```bash
# Fetch the repository's GraphQL ID
REPO_ID=$(gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      id
    }
  }
' -f owner='wu-changxing' -f repo='connectonion' --jq '.data.repository.id')

echo "Repository ID: $REPO_ID"
```

#### Step 8b: Get Discussion Category ID
```bash
# Find "Announcements" category ID
CATEGORY_ID=$(gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      discussionCategories(first: 20) {
        nodes {
          id
          name
        }
      }
    }
  }
' -f owner='wu-changxing' -f repo='connectonion' \
  --jq '.data.repository.discussionCategories.nodes[] | select(.name=="Announcements") | .id')

# Check if category exists
if [ -z "$CATEGORY_ID" ]; then
  echo "⚠️  Warning: 'Announcements' category not found!"
  echo "📋 Available categories:"
  gh api graphql -f query='
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        discussionCategories(first: 20) {
          nodes { name }
        }
      }
    }
  ' -f owner='wu-changxing' -f repo='connectonion' \
    --jq '.data.repository.discussionCategories.nodes[].name'

  echo ""
  echo "ℹ️  Skipping discussion creation. You can create the category at:"
  echo "   https://github.com/wu-changxing/connectonion/discussions/categories"

  # Update TodoWrite to mark as skipped
  # Continue with rest of release process
  exit 0  # Don't fail the entire release
else
  echo "Category ID: $CATEGORY_ID"
fi
```

#### Step 8c: Create Discussion with GraphQL Mutation
```bash
# Prepare discussion body
DISCUSSION_BODY=$(cat <<'EOF'
# ConnectOnion v{VERSION} is now available! 🎉

{HIGHLIGHTS_FROM_RELEASE_NOTES}

## 🚀 Quick Install

\`\`\`bash
pip install --upgrade connectonion
\`\`\`

## 📖 What's New

{WHATS_CHANGED_SECTION}

## 🔗 Links

- [Release Notes](https://github.com/wu-changxing/connectonion/releases/tag/v{VERSION})
- [PyPI Package](https://pypi.org/project/connectonion/{VERSION}/)
- [Documentation](https://docs.connectonion.com)

## 💬 Feedback

Please share your thoughts and report any issues!
EOF
)

# Create discussion using GraphQL mutation
DISCUSSION_URL=$(gh api graphql -f query='
  mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
    createDiscussion(input: {
      repositoryId: $repositoryId
      categoryId: $categoryId
      title: $title
      body: $body
    }) {
      discussion {
        url
        title
        id
      }
    }
  }
' -f repositoryId="$REPO_ID" \
  -f categoryId="$CATEGORY_ID" \
  -f title="📦 ConnectOnion v{VERSION} Released!" \
  -f body="$DISCUSSION_BODY" \
  --jq '.data.createDiscussion.discussion.url')

echo "✅ Discussion created: $DISCUSSION_URL"

# Update TodoWrite
# - [x] Created GitHub Discussion (GraphQL)
```

#### Alternative: One-Liner Version (Advanced)
```bash
# If you're confident the category exists, combine all steps:
gh api graphql -f query='
  mutation($owner: String!, $repo: String!, $title: String!, $body: String!) {
    repository(owner: $owner, name: $repo) {
      id
      discussionCategories(first: 20) {
        nodes {
          id
          name
        }
      }
    }
  }
' -f owner='wu-changxing' -f repo='connectonion' \
  -f title="📦 ConnectOnion v{VERSION} Released!" \
  -f body="[announcement content]" | \
jq -r '.data.repository | .id as $repoId | (.discussionCategories.nodes[] | select(.name=="Announcements") | .id) as $catId | {repositoryId: $repoId, categoryId: $catId}'
# (This is a demonstration - use the step-by-step approach for reliability)
```

### Discord Webhook Notification

Send release announcement to Discord:

```bash
# Get current version from setup.py
VERSION=$(grep "version=" setup.py | head -1 | sed 's/.*version="\(.*\)".*/\1/')

# Customize these for each release:
DESCRIPTION="Your one-line highlight here"  # Main feature/change
CHANGE_1="First key change"
CHANGE_2="Second key change"
CHANGE_3="Third key change"
CHANGE_4="Fourth key change (optional)"

# Fetch download stats from pepy.tech
DOWNLOADS=$(curl -s "https://static.pepy.tech/personalized-badge/connectonion?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads" | grep -o 'textLength="170">[^<]*' | head -1 | sed 's/textLength="170">//')

# Production webhook URL
WEBHOOK_URL="https://discord.com/api/webhooks/1431899098570559548/BtMzyf6O_yD0Z68LmySGNkCF9424OKpGFU8kyN14NOkl7DNo3OWaeTcwMhg7X82W9-dw"

# Send Discord notification
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
  \"embeds\": [{
    \"title\": \"v${VERSION} Released\",
    \"url\": \"https://github.com/openonion/connectonion/releases/tag/v${VERSION}\",
    \"color\": 5814783,
    \"description\": \"> ${DESCRIPTION}\\n\\n\\n╭─ What's Changed ─╮\\n\\n▸ ${CHANGE_1}\\n▸ ${CHANGE_2}\\n▸ ${CHANGE_3}\\n▸ ${CHANGE_4}\\n\\n\\n━━━━━━━━━━━━━━━━━━━\\n\\n\\n**📦 Install**\\n\\\`\\\`\\\`\\npip install --upgrade connectonion\\n\\\`\\\`\\\`\\n\\n[PyPI](https://pypi.org/project/connectonion/${VERSION}/) • [GitHub](https://github.com/openonion/connectonion/releases/tag/v${VERSION}) • [Docs](https://docs.connectonion.com) • ${DOWNLOADS} downloads\",
    \"footer\": {
      \"text\": \"✨ Keep simple things simple, make complicated things possible  •  with love, connectonion 💚\"
    }
  }]
}"

echo "✅ Discord webhook sent"

# Update TodoWrite
# - [x] Sent Discord release announcement
```

**Test webhook URL** (for testing before production):
```bash
TEST_WEBHOOK="https://discord.com/api/webhooks/1205075460749271090/c1Y-XExJ4FZ1x4UOO1SXotHCrzwd3ofoprPepeNB8iiA1PciEyS1jR6j6uBdfAiC20Mj"
# Replace WEBHOOK_URL with TEST_WEBHOOK to test first
```

**Important:** Before running, customize these variables for your release:
- `DESCRIPTION` - One-line highlight of the main feature/change
- `CHANGE_1` through `CHANGE_4` - Key changes in this release (3-4 bullet points)

Example:
```bash
DESCRIPTION="Email functions now **\\\"let it crash\\\"** with clear error messages."
CHANGE_1="Email functions raise clear \`ValueError\` for missing API keys"
CHANGE_2="Removed config.toml dependency - now uses \`.env\` directly"
CHANGE_3="Fixed 32 failing tests from Windows compatibility work"
CHANGE_4="All 143 unit tests passing ✓"
```

## Step 9: Post-Release Verification

### Verify Installation
```bash
# Test fresh install in temp environment
python -m venv /tmp/test-release
source /tmp/test-release/bin/activate
pip install connectonion=={VERSION}
python -c "import connectonion; print(connectonion.__version__)"
deactivate
rm -rf /tmp/test-release
```

### Check All Links
```bash
# PyPI page
curl -I https://pypi.org/project/connectonion/{VERSION}/ | head -1

# GitHub release
curl -I https://github.com/wu-changxing/connectonion/releases/tag/v{VERSION} | head -1

# GitHub discussion (if created) - Use GraphQL
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      discussions(first: 1, orderBy: {field: CREATED_AT, direction: DESC}) {
        nodes {
          url
          title
          createdAt
        }
      }
    }
  }
' -f owner='wu-changxing' -f repo='connectonion' \
  --jq '.data.repository.discussions.nodes[0] | "Discussion: \(.title) (\(.url))"'
```

## Step 10: Update TodoWrite Final Status

**Mark all tasks complete:**
```
Release v{VERSION} Complete ✅:
- [x] Version bumped from {OLD} to {NEW}
- [x] Version files updated (2 files)
- [x] Release notes generated
- [x] Git commit and tag created
- [x] Pushed to GitHub
- [x] Package built (wheel + source)
- [x] Uploaded to PyPI
- [x] GitHub release created
- [x] Documentation site updated
- [x] Community announcement posted (GraphQL)
- [x] Installation verified

Next version will be: {NEXT_VERSION}
```

## Error Handling

### Common Issues

**1. PyPI Upload Fails (duplicate version)**
```bash
# If version already exists on PyPI, bump version again
# This shouldn't happen if we checked properly, but just in case
```

**2. Git Push Fails (behind remote)**
```bash
git pull --rebase origin main
git push origin main
git push origin v{VERSION}
```

**3. Build Fails**
```bash
# Check setup.py syntax
python setup.py check

# Try with verbose output
python setup.py sdist bdist_wheel --verbose
```

**4. GitHub Release Creation Fails**
```bash
# Ensure gh is authenticated
gh auth status

# Try again with --draft flag first
gh release create v{VERSION} --draft --title "Release v{VERSION}" ...
```

**5. GitHub Discussion Creation Fails (GraphQL)**
```bash
# Verify gh can access GraphQL API
gh api graphql -f query='{ viewer { login } }'

# Check if Discussions are enabled for the repo
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      hasDiscussionsEnabled
    }
  }
' -f owner='wu-changxing' -f repo='connectonion' --jq '.data.repository.hasDiscussionsEnabled'

# If false, enable discussions at:
# https://github.com/wu-changxing/connectonion/settings

# List available discussion categories
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      discussionCategories(first: 20) {
        nodes { name id }
      }
    }
  }
' -f owner='wu-changxing' -f repo='connectonion' --jq '.data.repository.discussionCategories.nodes'

# If "Announcements" doesn't exist, create it manually or use a different category
```

**6. GraphQL Query Errors**
```bash
# Enable verbose output to debug GraphQL issues
gh api graphql -f query='...' --include

# Test GraphQL query in GitHub's GraphQL Explorer:
# https://docs.github.com/en/graphql/overview/explorer

# Common GraphQL errors:
# - "NOT_FOUND" → Repository or category doesn't exist
# - "FORBIDDEN" → Missing permissions (needs repo or public_repo scope)
# - "UNPROCESSABLE" → Invalid input (check repositoryId and categoryId format)
```

## Best Practices

1. **Always test in dev environment first** - Run through release steps in a test branch
2. **Review VERSIONING.md** - Ensure version bump follows project rules
3. **Write good release notes** - Users appreciate clear communication
4. **Verify before announcing** - Check PyPI and GitHub release are live
5. **Keep it simple** - Don't over-automate; some manual review is good

## Example Usage

```bash
# Automatic version detection
/release auto

# Explicit PATCH bump (bug fixes, docs)
/release patch

# Explicit MINOR bump (new features)
/release minor

# Explicit MAJOR bump (breaking changes)
/release major
```

## Integration with VERSIONING.md

This command follows the rules defined in `/VERSIONING.md`:

**Current Strategy (from VERSIONING.md):**
- PATCH (X.Y.Z): Increment by 1, roll to MINOR at 10
- MINOR (X.Y.0): Increment when PATCH hits 10, or for new features
- MAJOR (X.0.0): Increment when MINOR hits 10, or for breaking changes

**Example Progression:**
```
0.2.1 → 0.2.2 → 0.2.3 → ... → 0.2.9 → 0.3.0 → 0.3.1 → ...
```

## Summary

This command automates the entire release process while maintaining quality:
- ✅ Follows semantic versioning rules
- ✅ Generates comprehensive release notes
- ✅ Publishes to PyPI automatically
- ✅ Creates GitHub releases and discussions
- ✅ Verifies deployment success
- ✅ Tracks progress with TodoWrite

**Time saved:** ~30 minutes per release
**Consistency:** 100% - no missed steps
**Traceability:** Full audit trail in git and GitHub
