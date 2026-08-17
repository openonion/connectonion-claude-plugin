---
name: deploy-oo-chat
description: Release the OIP-native @connectonion/react reader through its protected npm workflow, pin the reviewed package in O Chat, and verify the live Work Room with real browser evidence
allowed-tools: Bash, Read, Edit, Glob, Grep, Write
---

# Deploy oo-chat

O Chat has one ConnectOnion client dependency: `@connectonion/react`. The React
package owns the hooks, session store, browser identity, endpoint discovery, and
OIP WebSocket client. `connectonion-ts` is retired; do not inspect, build,
publish, pin, or restore it. The supported product flow is native Codex or
Claude Code provider events in Core → React's OIP normalizer → O Chat's Work
Room; the browser is a fail-closed reader, not a provider adapter.

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
- A local tarball can preflight React/O Chat integration but is not public-release
  evidence. Use the exact published registry artifact for the release journey.
- A visible O Chat change needs final-head desktop and narrow-phone screenshots
  in the PR body. Human review, not an image-existence gate, decides whether
  those screenshots are a useful representation of the change.

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

1. Connect and complete owner onboarding once; confirm it renders one invite-code
   field and one submit control.
2. Send a normal prompt and confirm one answer.
3. Ask Codex to complete a concrete eight-step coding journey: inspect, plan,
   write, compile, test, review or fix, rerun, and final result. Confirm a
   compact native card streams semantic child activity rather than raw terminal
   output.
4. Run the equivalent native Claude Code delegation. A one-message mock success
   is not acceptance evidence for either provider.
5. Open each Work Room during the run. It must lead with current progress and
   latest useful outcome, keep old detail folded, and preserve an independently
   usable history rather than making the parent transcript grow without bound.
6. Render a provider thumbnail only when the native provider supplied current,
   safe image evidence. Do not manufacture a screenshot or leak a local path.
7. For a pending approval, the compact card exposes one correlated "Review
   decision" entry point; authoritative Allow/Reject lives inside the Work
   Room. Stop must acknowledge only the matching provider invocation and fail
   closed when recovery data is damaged.
8. Capture both desktop and narrow-phone states, including the approval/Stop
   journey when the selected profile requests it. Confirm no horizontal overflow.
9. Confirm browser console has no O Chat/React errors and Host logs show only
   the OIP product path. Do not enable or test an alternate protocol surface.

Do not place invite codes, credentials, or private keys in logs, screenshots,
issues, or PRs.

## 5. Merge and verify production

Merge the green O Chat PR into `main`; that commit triggers the production
Vercel deployment. Check the deployment status and repeat the published-artifact
OIP acceptance against `https://chat.openonion.ai`.

Record the React version, npm dist-tag, React PR/tag/workflow, O Chat PR/deploy,
agent address, and screenshot paths in the release handoff.
