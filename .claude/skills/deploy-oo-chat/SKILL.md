---
name: deploy-oo-chat
description: Deploy oo-chat to production — publish @connectonion/react and/or connectonion to npm via GitHub Actions, update the oo-chat dependency, commit, push, verify the Vercel deploy
allowed-tools: Bash, Read, Edit, Glob, Grep, Write
---

# Deploy oo-chat

## The SDK is two packages

| Package | Repo | What it is |
|---|---|---|
| `@connectonion/react` | `/Users/changxing/project/OnCourse/platform/connectonion-react` | the React hooks — `useAgentForHuman`, `useVoiceInput`, the Zustand session store, browser identity |
| `connectonion` | `/Users/changxing/project/OnCourse/platform/connectonion-ts` | the layer underneath — `RemoteAgent`, the WebSocket protocol, `fetchAgentInfo`, types |

**oo-chat imports from `@connectonion/react` only.** `connectonion/react` was removed in
`connectonion@0.3.0` — if you are about to write or restore that import, it is the old shape.

`connectonion` is a **peer** of `@connectonion/react`, so an app installs exactly one copy of
each. Publish `connectonion` first when both changed; the React package builds against it.

## Version Numbering

Increment patch by 1 each time. When patch reaches 10, roll up:

```
0.2.3 → 0.2.4    0.2.9 → 0.3.0   (not 0.2.10)    0.9.9 → 1.0.0
```

Rule: **if incrementing would make any segment two digits, reset it to 0 and bump the one above.**

The two packages version independently.

## Steps

### 1. Build & test the package you changed

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-react   # or connectonion-ts
npx tsc --noEmit
npx jest
```

If anything fails, stop and fix.

### 2. Bump the version

Read `package.json`, apply the rules above, edit the version field.

If you changed `@connectonion/react` in a way that needs a newer core, also raise its
`peerDependencies.connectonion` range.

### 3. Commit and tag

```bash
git add -A
git commit -m "v{NEW_VERSION}"
git tag v{NEW_VERSION}
git push origin main && git push origin v{NEW_VERSION}
```

The `v*` tag triggers `.github/workflows/publish.yml`, which verifies the tag matches
`package.json`, runs the tests, builds, and publishes.

Neither repo holds an npm token — both use **npm trusted publishing (OIDC)**. GitHub Actions
exchanges a short-lived OIDC token for publish rights and the release carries a provenance
attestation. Nothing to rotate, no secret to leak. If a publish fails with
`404 Not Found - PUT`, the trusted publisher is not registered for that package on npmjs.com;
that is a web-only setting and only the package owner can add it.

### 4. Wait for the publish

```bash
gh run watch --repo openonion/connectonion-react --exit-status
npm view @connectonion/react version
```

### 5. Point oo-chat at the published version

```bash
cd /Users/changxing/project/OnCourse/platform/oo-chat
npm pkg set dependencies."@connectonion/react"="^{NEW_VERSION}"
npm install
npm run build          # MUST pass — this is what Vercel runs
npx vitest run
```

Confirm the lockfile resolved from the registry, not from a path:

```bash
grep -A2 '"node_modules/@connectonion/react"' package-lock.json   # expect a registry URL
```

### 6. Commit and push oo-chat

```bash
git add package.json package-lock.json
git commit -m "Update @connectonion/react to v{NEW_VERSION}"
git push
```

Pushing a branch builds a Vercel **preview**; merging to `main` builds **production**.

### 7. Verify on the preview before merging

```bash
vercel ls --limit 3
```

**A green local build is not the check.** See below.

## Never put a local path in package.json

Do not "restore a local dev link" by editing `package.json` to `file:../connectonion-ts` or
`file:../connectonion-react`, and never run `npm i <local-path>` in a package you are about
to publish — `npm i <path>` rewrites `package.json` as a side effect.

That is not a style preference; it has broken production three times:

- `RemoteSessionStatus = 'running'` — local build green, Vercel red (fixed by `connectonion@0.1.6`)
- `profile` — same shape (fixed by `0.1.10`)
- `@connectonion/react@0.2.2` — published with `peerDependencies` still pointing at
  `file:/tmp/...`. `tsc`, 30 tests, and the build were all green; the package was
  **uninstallable for every consumer**. Nothing in a repo's own test suite installs the
  package the way a consumer does.

A symlinked or path dependency typechecks against unreleased code. The published semver is
what Vercel installs. **Publish first, then bump.** If you must symlink for local iteration,
symlink inside `node_modules` only and never commit it.

## Key Info

| Item | Value |
|------|-------|
| React repo | `openonion/connectonion-react` → npm `@connectonion/react` |
| TS SDK repo | `openonion/connectonion-ts` → npm `connectonion` |
| oo-chat repo | `openonion/oo-chat` |
| Vercel project | `oo-chat` |
| Publish trigger | git tag `v*` → GitHub Actions → npm (OIDC, no token) |
| Deploy trigger | push to `main` → Vercel production; branch push → preview |
| What oo-chat imports | `@connectonion/react` only |
| Production deps | `"@connectonion/react": "^X.Y.Z"` + `"connectonion": "^X.Y.Z"` (its peer) |
