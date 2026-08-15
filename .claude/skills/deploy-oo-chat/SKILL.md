---
name: deploy-oo-chat
description: Release @connectonion/react through its protected npm workflow, pin the reviewed package in oo-chat, merge, and verify the Vercel deployment with a real browser session
allowed-tools: Bash, Read, Edit, Glob, Grep, Write
---

# Deploy oo-chat

O Chat has one ConnectOnion client dependency: `@connectonion/react`. The React
package owns the hooks, session store, browser identity, endpoint discovery, and
OIP WebSocket client. `connectonion-ts` is retired; do not inspect, build,
publish, pin, or restore it.

| Project | Repository | Published artifact |
|---|---|---|
| React client | `openonion/connectonion-react` | `@connectonion/react` |
| O Chat | `openonion/oo-chat` | Vercel application |

## Rules

- Start from clean branches based on the latest `origin/main` in both repos.
- Never publish from a workstation. Merge reviewed code, then push an exact
  `v<package-version>` tag at the current React `main` commit.
- The React workflow derives the npm dist-tag from the version: `alpha`,
  `beta`, `rc`, or `latest`.
- Do not move a published tag. If a release is wrong, make a new version.
- O Chat pins an exact prerelease. Do not use `^` for alpha/beta/RC builds.
- Never put a `file:` dependency in either `package.json` or lockfile.
- Do not merge O Chat until the npm registry serves the reviewed React version.
- A green build is necessary but not sufficient: finish with an OIP browser E2E
  against the deployed preview, then repeat it against production.

## 1. Prepare and review the React release

```bash
cd /Users/changxing/project/OnCourse/platform/connectonion-react
git fetch origin
git switch -c fix/<topic> origin/main
npm ci
npm run typecheck
npm test
npm run build
```

For a release, update `package.json` and `package-lock.json` to the next SemVer
version. Preserve normal numeric ordering; `0.4.2` may advance to `0.4.3` and
does not need a made-up digit rollover. Use canonical prereleases such as
`0.4.3-alpha.1`.

Open a PR, wait for required checks, and merge it. Confirm the merge commit is
the current reviewed `main` before tagging.

## 2. Tag and verify the protected npm release

```bash
git switch main
git pull --ff-only origin main
node -p "require('./package.json').version"
git tag v<version>
git push origin v<version>
gh run watch --repo openonion/connectonion-react --exit-status
```

`.github/workflows/publish.yml` checks that the tag equals `package.json`, the
tag points at current `main`, dependencies audit cleanly, typecheck/tests/build
pass, and the exact packed artifact installs in a clean project. It publishes
with npm Trusted Publishing and provenance.

Verify the public artifact and expected dist-tag:

```bash
npm view @connectonion/react@<version> version dist.tarball dist.integrity
npm view @connectonion/react dist-tags --json
```

## 3. Pin O Chat to the public package

```bash
cd /Users/changxing/project/OnCourse/platform/oo-chat
git fetch origin
git switch -c fix/<topic> origin/main
npm pkg set dependencies."@connectonion/react"="<version>"
npm install --package-lock-only
npm ci
npm run lint
npm test
npm run build
```

Confirm both manifests use the same exact version and the lockfile resolves a
registry tarball:

```bash
node -e "const p=require('./package.json'); const l=require('./package-lock.json'); console.log(p.dependencies['@connectonion/react'], l.packages['node_modules/@connectonion/react'])"
```

Open an O Chat PR and let its branch produce the Vercel preview. Test the actual
preview URL before merging.

## 4. Published-artifact OIP acceptance

Start `co ai` from the matching Python preview/stable package, not an editable
checkout. Open its O Chat link in a dedicated browser tab and preserve Host logs
plus screenshots. At minimum:

1. Connect and complete owner onboarding once.
2. Send a normal prompt and confirm one answer.
3. Ask the agent to delegate a concrete task to Codex and confirm the Codex card,
   streamed child activity, and final result.
4. If Claude Code changed, run the equivalent Claude Code delegation.
5. Confirm the browser console has no O Chat/React errors and Host logs show OIP
   `/ws`, not ACP.
6. Confirm initial onboarding renders one invite-code field and one submit.

Do not place invite codes, credentials, or private keys in logs, screenshots,
issues, or PRs.

## 5. Merge and verify production

Merge the green O Chat PR into `main`; that commit triggers the production
Vercel deployment. Check the deployment status and repeat the published-artifact
OIP acceptance against `https://chat.openonion.ai`.

Record the React version, npm dist-tag, React PR/tag/workflow, O Chat PR/deploy,
agent address, and screenshot paths in the release handoff.
