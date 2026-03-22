---
name: deploy-oo-chat
description: Deploy oo-chat to production — publish connectonion-ts to npm via GitHub Actions, update oo-chat dependency, commit, push, verify Vercel deploy
allowed-tools: Bash, Read, Edit, Glob, Grep, Write
---

# Deploy oo-chat

Publish the connectonion TypeScript SDK and deploy oo-chat to Vercel.

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

### 1. Build & test connectonion-ts

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-ts
./node_modules/.bin/tsc
npx jest tests/connect.test.ts --forceExit
```

If tests fail, stop and fix.

### 2. Bump version in connectonion-ts

Read `package.json` version. Apply versioning rules above. Edit the version field.

### 3. Commit and tag

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-ts
git add -A
git commit -m "v{NEW_VERSION}"
git tag v{NEW_VERSION}
git push && git push --tags
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

Edit `oo-chat/package.json`:
- Change `"connectonion": "file:../connectonion-ts"` → `"connectonion": "^{NEW_VERSION}"`

```bash
cd /Users/changxing/project/OnCourse/platform/oo-chat
npm install
```

### 6. Commit and push oo-chat

```bash
git add package.json package-lock.json
git commit -m "Update connectonion to v{NEW_VERSION}"
git push
```

Pushing to main triggers Vercel auto-deploy.

### 7. Verify Vercel deployment

```bash
vercel ls --limit 3
```

### 8. Restore local dev link

After deploy, restore for local development:

Edit `oo-chat/package.json`:
- Change `"connectonion": "^{NEW_VERSION}"` → `"connectonion": "file:../connectonion-ts"`

```bash
npm install
```

Don't commit this — local dev only.

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
