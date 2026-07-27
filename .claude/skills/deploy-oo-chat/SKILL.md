---
name: deploy-oo-chat
description: Publish connectonion-ts and deploy oo-chat to production. Use when the user explicitly requests the oo-chat release workflow from Claude Code or co ai; supports a no-write --dry-run preflight.
tools:
  - Bash(cd *)
  - Bash(git *)
  - Bash(./node_modules/.bin/tsc)
  - Bash(npx jest *)
  - Bash(npm *)
  - Bash(gh *)
  - Bash(vercel *)
  - read
  - edit
---

# Deploy oo-chat

Publish the connectonion TypeScript SDK and deploy oo-chat to Vercel.

## Invocation

Claude Code:

```text
/connectonion:deploy-oo-chat
/connectonion:deploy-oo-chat --dry-run
```

ConnectOnion, from this plugin repository or another project containing this
skill under `.claude/skills/`:

```bash
co ai --yolo "/deploy-oo-chat" --yolo-turns 20
co ai --yolo "/deploy-oo-chat --dry-run" --yolo-turns 5
```

## Safety contract

- Treat a normal invocation as authorization for the named release only.
- Stop if either repository contains unrelated changes. Never stage, overwrite,
  discard, or commit them.
- Never force-push, replace an existing tag, bypass hooks, or publish from a
  branch other than `main`.
- If the arguments contain `--dry-run`, perform only Step 0 and report the
  release plan. Do not edit files, install packages, commit, tag, push, trigger
  workflows, publish to npm, or invoke Vercel.
- Automated validation and forward tests must use `--dry-run`.

## Version Numbering

Increment patch by 1 each time. When patch reaches 10, roll up:

```
0.0.8  → 0.0.9
0.0.9  → 0.1.0   (not 0.0.10)
0.1.8  → 0.1.9
0.1.9  → 0.2.0
0.9.9  → 1.0.0
```

Rule: **if incrementing would make any segment two digits, reset it to 0 and bump the one above.**

## Steps

### 0. Preflight

Use these repositories:

- `/Users/changxing/project/OnCourse/platform/connectonion-ts`
- `/Users/changxing/project/OnCourse/platform/oo-chat`

For both repositories, inspect `git status -sb`, confirm the checked-out branch
is `main`, and confirm `origin` points to the expected `openonion` repository.
Compare local `HEAD` with `git ls-remote origin refs/heads/main` without
fetching. Stop on unrelated changes, an unexpected branch/remote, or a local
branch that is not exactly at the live remote `main`.

Read the current `connectonion-ts/package.json` version, calculate the next
version using the rules below, and confirm the target tag does not already
exist locally or on the remote. Read and retain oo-chat's exact current
`connectonion` dependency value. Report the exact files and commands the release
would change.

For `--dry-run`, stop here. The successful result is the preflight report; no
repository or external state may change.

### 1. Build and test connectonion-ts

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-ts
./node_modules/.bin/tsc
npx jest tests/connect.test.ts --forceExit
```

If tests fail, stop and fix.

### 2. Bump version in connectonion-ts

Apply the versioning rules above, then update both `package.json` and
`package-lock.json` without running package lifecycle scripts:

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-ts
npm version {NEW_VERSION} --no-git-tag-version --ignore-scripts
```

Verify the root version in both files is exactly `{NEW_VERSION}` before
committing.

### 3. Commit and tag

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-ts
git add package.json package-lock.json
git commit -m "v{NEW_VERSION}"
git tag v{NEW_VERSION}
git push origin main
git push origin v{NEW_VERSION}
```

The `v*` tag push triggers GitHub Actions (`.github/workflows/publish.yml`) which builds and publishes to npm automatically.

### 4. Wait for npm publish

```bash
gh run list --limit 1 --repo openonion/connectonion-ts
gh run watch --repo openonion/connectonion-ts
```

Wait until workflow succeeds. Verify:

```bash
npm view connectonion version
```

### 5. Update oo-chat dependency

```bash
cd /Users/changxing/project/OnCourse/platform/oo-chat
npm install "connectonion@^{NEW_VERSION}"
```

Verify both `package.json` and `package-lock.json` resolve the requested
production dependency before committing.

### 6. Commit and push oo-chat

```bash
git add package.json package-lock.json
git commit -m "Update connectonion to v{NEW_VERSION}"
git push origin main
```

Pushing to main triggers Vercel auto-deploy.

### 7. Verify Vercel deployment

```bash
vercel ls --limit 3
```

### 8. Restore an original local dev link

If and only if the preflight dependency started with `file:`, restore that exact
original dependency after deployment:

```text
npm install "connectonion@{ORIGINAL_DEPENDENCY}"
```

Do not commit this local-only restoration. If the original dependency was a
registry version, leave the deployed version in place and require a clean
working tree.

## Key Info

| Item | Value |
|------|-------|
| TS SDK repo | `openonion/connectonion-ts` |
| oo-chat repo | `openonion/oo-chat` |
| npm package | `connectonion` |
| Vercel project | `oo-chat` |
| Publish trigger | Git tag `v*` → GitHub Actions |
| Deploy trigger | Push to main → Vercel |
| Local dev dep | `"connectonion": "file:../connectonion-ts"` |
| Production dep | `"connectonion": "^X.Y.Z"` |
