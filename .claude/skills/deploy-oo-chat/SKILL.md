---
name: deploy-oo-chat
description: Publish connectonion-ts to npm and deploy oo-chat to Vercel production. Use only when the user explicitly asks for the complete production release.
---

# Deploy oo-chat

Publish the ConnectOnion TypeScript SDK, update oo-chat to the published
version, and verify the production deployment.

This workflow mutates exactly these production targets:

- GitHub repository `openonion/connectonion-ts`
- GitHub repository `openonion/oo-chat`
- npm package `connectonion`
- Vercel project `oo-chat`

Do not deploy any other repository, package, project, or environment.

## Invocation

Claude Code:

```text
$connectonion:deploy-oo-chat
```

ConnectOnion AI, from the `connectonion-claude-plugin` repository:

```bash
co ai --yolo --yolo-turns 25 "/deploy-oo-chat"
```

Before doing anything else, require `co ai --help` to contain the separate
options `--yolo` and `--yolo-turns`. If either is absent, stop and ask the user
to upgrade ConnectOnion. Never silently fall back to an unbounded run.

Invoking this skill is authorization only for the production actions above.
YOLO removes routine approval prompts; it does not authorize force pushes, tag
replacement, unrelated edits, bypassed checks, or any broader target.

## Execution contract

- Fail closed. Start every shell call with `set -euo pipefail`.
- Shell calls are isolated. Define absolute `TS_REPO` and `CHAT_REPO` paths in
  every call; never assume variables or `cd` persist.
- Use the Git common directory when resolving the platform root. This also
  works when the plugin is running from a linked worktree.
- Before the first mutation, both repositories must be clean, on `main`, and
  exactly synchronized with freshly fetched `origin/main`.
- Never stash, reset, clean, switch branches, force push, replace a tag, or
  print credentials or environment files.
- Stage only the files named below.
- Stop immediately when any assertion, install, test, build, push, publish, or
  deployment check fails.
- All discovery and publication polling must have a finite retry count.
- If failure occurs after a public push, report the exact published state. Do
  not attempt an unrequested rollback.

## 0. Resolve and verify

Run this as one fail-closed shell call:

```bash
set -euo pipefail

HELP_OUTPUT="$(NO_COLOR=1 TERM=dumb co ai --help)"
grep -Eq '(^|[[:space:]])--yolo([[:space:]]|$)' <<<"$HELP_OUTPUT"
grep -Eq '(^|[[:space:]])--yolo-turns([[:space:]]|$)' <<<"$HELP_OUTPUT"

COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"
CHAT_REPO="$PLATFORM_ROOT/oo-chat"

test -d "$TS_REPO/.git"
test -d "$CHAT_REPO/.git"

case "$(git -C "$TS_REPO" remote get-url origin)" in
  https://github.com/openonion/connectonion-ts.git|git@github.com:openonion/connectonion-ts.git) ;;
  *) echo "Unexpected connectonion-ts origin" >&2; exit 1 ;;
esac
case "$(git -C "$CHAT_REPO" remote get-url origin)" in
  https://github.com/openonion/oo-chat.git|git@github.com:openonion/oo-chat.git) ;;
  *) echo "Unexpected oo-chat origin" >&2; exit 1 ;;
esac

git -C "$TS_REPO" fetch origin
git -C "$CHAT_REPO" fetch origin

test "$(git -C "$TS_REPO" branch --show-current)" = "main"
test "$(git -C "$CHAT_REPO" branch --show-current)" = "main"
test -z "$(git -C "$TS_REPO" status --porcelain)"
test -z "$(git -C "$CHAT_REPO" status --porcelain)"
test "$(git -C "$TS_REPO" rev-parse HEAD)" = \
  "$(git -C "$TS_REPO" rev-parse origin/main)"
test "$(git -C "$CHAT_REPO" rev-parse HEAD)" = \
  "$(git -C "$CHAT_REPO" rev-parse origin/main)"

gh auth status
PUBLISHED_VERSION="$(npm view connectonion version)"
test -n "$PUBLISHED_VERSION"
vercel whoami --cwd "$CHAT_REPO"
test -f "$CHAT_REPO/.vercel/project.json"
test "$(node -p "require('$CHAT_REPO/.vercel/project.json').projectName")" = "oo-chat"
```

If repository discovery fails, locate the two exact Git roots inside the
user's workspace, then substitute their absolute paths in every later call.
Do not search outside the workspace. Report any branch, cleanliness, or SHA
mismatch and stop; do not repair the user's worktree.

## Version policy

Read `connectonion-ts/package.json` and increment patch with decimal carry at
9:

```text
0.0.8 → 0.0.9
0.0.9 → 0.1.0
0.1.9 → 0.2.0
0.9.9 → 1.0.0
```

Before editing, compute and validate the candidate in a self-contained call:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"

CURRENT_VERSION="$(node -p "require('$TS_REPO/package.json').version")"
PUBLISHED_VERSION="$(npm view connectonion version)"
test "$CURRENT_VERSION" = "$PUBLISHED_VERSION"

NEW_VERSION="$(node -e '
const parts = process.argv[1].split(".").map(Number);
if (parts.length !== 3 || parts.some((n) => !Number.isInteger(n) || n < 0 || n > 9)) {
  throw new Error("version must contain three single-digit segments");
}
for (let i = 2; i >= 0; i -= 1) {
  if (parts[i] < 9) {
    parts[i] += 1;
    process.stdout.write(parts.join("."));
    process.exit(0);
  }
  parts[i] = 0;
}
throw new Error("version policy is undefined after 9.9.9");
' "$CURRENT_VERSION")"

LOCAL_TAG="$(git -C "$TS_REPO" tag -l "v$NEW_VERSION")"
REMOTE_TAG="$(git -C "$TS_REPO" ls-remote --tags origin "refs/tags/v$NEW_VERSION")"
test -z "$LOCAL_TAG"
test -z "$REMOTE_TAG"

NPM_VERSIONS="$(npm view connectonion versions --json)"
if node -e '
const value = JSON.parse(process.argv[1]);
const versions = Array.isArray(value) ? value : [value];
process.exit(versions.includes(process.argv[2]) ? 0 : 1);
' "$NPM_VERSIONS" "$NEW_VERSION"; then
  echo "connectonion@$NEW_VERSION already exists" >&2
  exit 1
fi
printf 'Release candidate: %s -> %s\n' "$CURRENT_VERSION" "$NEW_VERSION"
```

Never reuse a version that exists in Git or npm.

## 1. Test the SDK

`connectonion-ts` intentionally ignores `package-lock.json`, and its publish
workflow uses `npm install`. Do not use `npm ci` or stage the ignored lockfile.
Ignore any stale local lock during validation:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"

npm --prefix "$TS_REPO" install --package-lock=false
npm --prefix "$TS_REPO" run lint
npm --prefix "$TS_REPO" run build
npm --prefix "$TS_REPO" test -- --runInBand --forceExit
test -z "$(git -C "$TS_REPO" status --porcelain)"
```

## 2. Bump and preflight oo-chat locally

Bump only `connectonion-ts/package.json`, pack the unpublished SDK, and test it
against a disposable oo-chat worktree before any public push:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"
CHAT_REPO="$PLATFORM_ROOT/oo-chat"

CURRENT_VERSION="$(node -p "require('$TS_REPO/package.json').version")"
NEW_VERSION="$(node -e '
const parts = process.argv[1].split(".").map(Number);
for (let i = 2; i >= 0; i -= 1) {
  if (parts[i] < 9) {
    parts[i] += 1;
    process.stdout.write(parts.join("."));
    process.exit(0);
  }
  parts[i] = 0;
}
throw new Error("version policy is undefined after 9.9.9");
' "$CURRENT_VERSION")"

npm --prefix "$TS_REPO" pkg set "version=$NEW_VERSION"
test "$(git -C "$TS_REPO" diff --name-only)" = "package.json"
git -C "$TS_REPO" diff --check

PREFLIGHT_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/oo-chat-preflight.XXXXXX")"
CHAT_PREFLIGHT="$PREFLIGHT_ROOT/oo-chat"
cleanup_preflight() {
  git -C "$CHAT_REPO" worktree remove --force "$CHAT_PREFLIGHT" >/dev/null 2>&1 || true
  case "$PREFLIGHT_ROOT" in
    "${TMPDIR:-/tmp}"/oo-chat-preflight.*) rm -rf "$PREFLIGHT_ROOT" ;;
    *) echo "Refusing to remove unexpected temp path" >&2 ;;
  esac
}
trap cleanup_preflight EXIT

npm --prefix "$TS_REPO" pack --pack-destination "$PREFLIGHT_ROOT"
PACK_FILE="$PREFLIGHT_ROOT/connectonion-$NEW_VERSION.tgz"
test -f "$PACK_FILE"

git -C "$CHAT_REPO" worktree add --detach "$CHAT_PREFLIGHT" origin/main
npm --prefix "$CHAT_PREFLIGHT" ci
npm --prefix "$CHAT_PREFLIGHT" install --save "$PACK_FILE"
test "$(node -p "require('$CHAT_PREFLIGHT/node_modules/connectonion/package.json').version")" = \
  "$NEW_VERSION"
npm --prefix "$CHAT_PREFLIGHT" run lint
npm --prefix "$CHAT_PREFLIGHT" run build
```

The trap may remove only the `mktemp` directory and its disposable worktree.
It must never remove either real repository. If preflight fails, stop with the
SDK bump still local and unpublished.

## 3. Commit, tag, and publish the SDK

Recheck the remote race, commit only `package.json`, tag it, then push `main`
and the tag atomically:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"
CHAT_REPO="$PLATFORM_ROOT/oo-chat"
NEW_VERSION="$(node -p "require('$TS_REPO/package.json').version")"

git -C "$TS_REPO" fetch origin
git -C "$CHAT_REPO" fetch origin
test "$(git -C "$TS_REPO" rev-parse HEAD)" = \
  "$(git -C "$TS_REPO" rev-parse origin/main)"
test "$(git -C "$CHAT_REPO" branch --show-current)" = "main"
test -z "$(git -C "$CHAT_REPO" status --porcelain)"
test "$(git -C "$CHAT_REPO" rev-parse HEAD)" = \
  "$(git -C "$CHAT_REPO" rev-parse origin/main)"

LOCAL_TAG="$(git -C "$TS_REPO" tag -l "v$NEW_VERSION")"
REMOTE_TAG="$(git -C "$TS_REPO" ls-remote --tags origin "refs/tags/v$NEW_VERSION")"
test -z "$LOCAL_TAG"
test -z "$REMOTE_TAG"

NPM_VERSIONS="$(npm view connectonion versions --json)"
if node -e '
const value = JSON.parse(process.argv[1]);
const versions = Array.isArray(value) ? value : [value];
process.exit(versions.includes(process.argv[2]) ? 0 : 1);
' "$NPM_VERSIONS" "$NEW_VERSION"; then
  echo "connectonion@$NEW_VERSION already exists" >&2
  exit 1
fi

test "$(git -C "$TS_REPO" diff --name-only)" = "package.json"
git -C "$TS_REPO" diff --check
git -C "$TS_REPO" add package.json
test "$(git -C "$TS_REPO" diff --cached --name-only)" = "package.json"
git -C "$TS_REPO" diff --cached --check
git -C "$TS_REPO" commit -m "v$NEW_VERSION"
git -C "$TS_REPO" tag "v$NEW_VERSION"
SDK_SHA="$(git -C "$TS_REPO" rev-parse HEAD)"
git -C "$TS_REPO" push --atomic origin main "v$NEW_VERSION"
printf 'SDK_SHA=%s\n' "$SDK_SHA"
```

The `v*` tag triggers `.github/workflows/publish.yml`.

## 4. Verify GitHub Actions and npm

Discover only a push run matching the exact tag and commit. Poll at most ten
minutes, then poll the selected run at most thirty minutes:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"
NEW_VERSION="$(node -p "require('$TS_REPO/package.json').version")"
SDK_SHA="$(git -C "$TS_REPO" rev-parse "v$NEW_VERSION^{commit}")"

RUN_ID=""
for attempt in $(seq 1 60); do
  RUN_MATCHES="$(gh run list \
    --repo openonion/connectonion-ts \
    --workflow publish.yml \
    --event push \
    --branch "v$NEW_VERSION" \
    --commit "$SDK_SHA" \
    --limit 20 \
    --json databaseId,event,headBranch,headSha \
    --jq ".[] | select(.event == \"push\" and .headBranch == \"v$NEW_VERSION\" and .headSha == \"$SDK_SHA\") | .databaseId")"
  RUN_ID="$(awk 'NR == 1 {print}' <<<"$RUN_MATCHES")"
  test -n "$RUN_ID" && break
  sleep 10
done
test -n "$RUN_ID"

RUN_STATUS=""
RUN_CONCLUSION=""
for attempt in $(seq 1 120); do
  RUN_STATUS="$(gh run view "$RUN_ID" \
    --repo openonion/connectonion-ts --json status --jq .status)"
  if test "$RUN_STATUS" = "completed"; then
    RUN_CONCLUSION="$(gh run view "$RUN_ID" \
      --repo openonion/connectonion-ts --json conclusion --jq .conclusion)"
    break
  fi
  sleep 15
done
test "$RUN_STATUS" = "completed"
test "$RUN_CONCLUSION" = "success"
RUN_URL="$(gh run view "$RUN_ID" \
  --repo openonion/connectonion-ts --json url --jq .url)"

NPM_VERSION=""
for attempt in $(seq 1 60); do
  NPM_VERSION="$(npm view "connectonion@$NEW_VERSION" version 2>/dev/null || true)"
  test "$NPM_VERSION" = "$NEW_VERSION" && break
  sleep 10
done
test "$NPM_VERSION" = "$NEW_VERSION"
printf 'RUN_URL=%s\n' "$RUN_URL"
```

Do not modify oo-chat until both the exact workflow run and npm version pass.

## 5. Update and push oo-chat

Install the published compatible range, validate the only two expected files,
then recheck `origin/main` before committing:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
TS_REPO="$PLATFORM_ROOT/connectonion-ts"
CHAT_REPO="$PLATFORM_ROOT/oo-chat"
NEW_VERSION="$(node -p "require('$TS_REPO/package.json').version")"

npm --prefix "$CHAT_REPO" install --save "connectonion@^$NEW_VERSION"
test "$(node -p "require('$CHAT_REPO/package.json').dependencies.connectonion")" = \
  "^$NEW_VERSION"
test "$(git -C "$CHAT_REPO" diff --name-only | sort)" = \
  "$(printf '%s\n' package-lock.json package.json | sort)"
git -C "$CHAT_REPO" diff --check
npm --prefix "$CHAT_REPO" run lint
npm --prefix "$CHAT_REPO" run build

git -C "$CHAT_REPO" fetch origin
test "$(git -C "$CHAT_REPO" rev-parse HEAD)" = \
  "$(git -C "$CHAT_REPO" rev-parse origin/main)"
git -C "$CHAT_REPO" add package.json package-lock.json
test "$(git -C "$CHAT_REPO" diff --cached --name-only | sort)" = \
  "$(printf '%s\n' package-lock.json package.json | sort)"
git -C "$CHAT_REPO" diff --cached --check
git -C "$CHAT_REPO" commit -m "Update connectonion to v$NEW_VERSION"
CHAT_SHA="$(git -C "$CHAT_REPO" rev-parse HEAD)"
git -C "$CHAT_REPO" push origin main
printf 'CHAT_SHA=%s\n' "$CHAT_SHA"
```

Pushing `main` triggers Vercel production deployment.

## 6. Verify the exact Vercel deployment

Filter by the pushed Git SHA and accept the result only when exactly one
deployment URL is returned. Poll for ten minutes:

```bash
set -euo pipefail
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
PLATFORM_ROOT="$(dirname "$(dirname "$COMMON_DIR")")"
CHAT_REPO="$PLATFORM_ROOT/oo-chat"
CHAT_SHA="$(git -C "$CHAT_REPO" rev-parse HEAD)"
CANONICAL_URL="https://chat.openonion.ai/"

DEPLOYMENT_URL=""
for attempt in $(seq 1 60); do
  DEPLOYMENTS="$(vercel list oo-chat \
    --environment production \
    --meta "githubCommitSha=$CHAT_SHA" \
    --yes --no-color --cwd "$CHAT_REPO")"
  URL_COUNT="$(grep -Ec '^https://[^[:space:]]+$' <<<"$DEPLOYMENTS" || true)"
  if test "$URL_COUNT" = "1"; then
    DEPLOYMENT_URL="$(grep -E '^https://[^[:space:]]+$' <<<"$DEPLOYMENTS")"
    break
  fi
  sleep 10
done
test -n "$DEPLOYMENT_URL"

vercel inspect "$DEPLOYMENT_URL" \
  --wait --timeout 10m --no-color --cwd "$CHAT_REPO"

DEPLOYMENT_OUTPUT="$(vercel inspect "$DEPLOYMENT_URL" \
  --no-color --cwd "$CHAT_REPO" 2>&1)"
DEPLOYMENT_ID="$(awk '$1 == "id" {print $2}' <<<"$DEPLOYMENT_OUTPUT")"
test -n "$DEPLOYMENT_ID"

CANONICAL_ID=""
for attempt in $(seq 1 60); do
  CANONICAL_OUTPUT="$(vercel inspect "$CANONICAL_URL" \
    --no-color --cwd "$CHAT_REPO" 2>&1 || true)"
  CANONICAL_ID="$(awk '$1 == "id" {print $2; exit}' <<<"$CANONICAL_OUTPUT")"
  test "$CANONICAL_ID" = "$DEPLOYMENT_ID" && break
  sleep 10
done
test "$CANONICAL_ID" = "$DEPLOYMENT_ID"

SMOKE_BODY="$(mktemp "${TMPDIR:-/tmp}/oo-chat-smoke.XXXXXX")"
trap 'rm -f "$SMOKE_BODY"' EXIT
FINAL_URL="$(curl --fail --silent --show-error --location \
  --max-time 30 --output "$SMOKE_BODY" --write-out '%{url_effective}' \
  "$CANONICAL_URL")"
test "$FINAL_URL" = "$CANONICAL_URL"
grep -Fq 'oo-chat - Open Source AI Chat Client' "$SMOKE_BODY"

test -z "$(git -C "$CHAT_REPO" status --porcelain)"
test -z "$(git -C "$PLATFORM_ROOT/connectonion-ts" status --porcelain)"
printf 'DEPLOYMENT_URL=%s\n' "$DEPLOYMENT_URL"
```

The unique Vercel deployment URL may require authentication, so do not treat
its HTTP `200` login page as a smoke test. The canonical alias must resolve to
the same deployment ID and return the expected public app content.

Do not restore a local `file:../connectonion-ts` dependency. oo-chat keeps the
published npm range in both package manifests.

## Completion report

Report:

- Published npm version
- connectonion-ts commit and tag
- Exact GitHub Actions run URL and conclusion
- oo-chat commit
- Matching Vercel deployment URL and state
- Canonical production smoke-check result
- Final clean-worktree confirmation

If anything failed after a public push, also state exactly what already
published or deployed. Do not delete a tag, force push, deprecate npm, or roll
back unless the user separately authorizes that recovery.
