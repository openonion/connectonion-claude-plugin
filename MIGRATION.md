# Migration to Skills Format (v1.1.0)

## What Changed

The ConnectOnion Claude plugin has been migrated from the old commands format to the modern skills format.

### Before (v1.0.x)
```
connectonion-claude-plugin/
├── .claude-plugin/
│   └── plugin.json  (pointed to ./commands)
└── commands/
    ├── aaron-build-my-agent.md
    ├── aaron-review-my-code.md
    └── ...
```

### After (v1.1.0)
```
connectonion-claude-plugin/
├── .claude-plugin/
│   └── plugin.json  (now points to ./.claude/skills)
├── .claude/
│   └── skills/
│       ├── aaron-build-my-agent/
│       │   └── SKILL.md
│       ├── aaron-review-my-code/
│       │   └── SKILL.md
│       └── ...
└── commands/  (deprecated, kept for reference)
```

## Available Skills

All skills are prefixed with `connectonion:` in the global namespace:

- **connectonion:aaron-build-my-agent** - Let Aaron build your agent from simple to complex
- **connectonion:aaron-review-my-code** - Get reviewed by Aaron (ConnectOnion creator)
- **connectonion:design-refine** - Analyze and iteratively refine website design
- **connectonion:generate-code-map-headers** - Add documentation headers to code files
- **connectonion:linus-review-my-code** - Get brutally honest code review

## Using the Skills

Skills are automatically available in Claude Code through symlinks in `~/.claude/skills/`:

```bash
# Use a skill
/aaron-review-my-code

# Or use the full name
/connectonion:aaron-review-my-code
```

## For Plugin Developers

If you're maintaining a fork or custom version:

1. Skills live in `.claude/skills/{skill-name}/SKILL.md`
2. Each SKILL.md has YAML frontmatter:
   ```yaml
   ---
   description: Short description here
   allowed-tools: Read, Write, Edit
   argument-hint: <optional-arguments>
   ---
   ```
3. Plugin.json should reference skills: `"skills": "./.claude/skills"`
4. Create symlinks: `ln -s /path/to/skill ~/.claude/skills/namespace:skill-name`

## Backwards Compatibility

The old `commands/` directory is preserved but deprecated. Future updates will only modify `.claude/skills/`.
