# CI / Release Guide

This document explains the GitHub Actions release workflow, how the
`CHANGELOG.md` is updated, and common troubleshooting steps for maintainers.

## Overview

The release workflow triggers on tag pushes that match `v*` and runs in
three phases:

- Prepare: runs `.github/scripts/generate-release-notes.js` to generate the
  release body and write an updated `CHANGELOG.md`. The workflow then
  creates a pull request named `changelog/<tag>` with the changelog update.
- Build: builds platform artifacts (PyInstaller) on `ubuntu-latest` and
  `windows-latest`. The job checks out full history (`fetch-depth: 0`).
- Release: generates final release notes and creates a GitHub Release,
  attaching the built artifacts.

## Changelog PR flow

1. Push an annotated tag from your local clone:

```bash
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

2. The `prepare` job will run and open a PR branch `changelog/v0.3.0`
   containing an updated `CHANGELOG.md` with a `## [0.3.0] — <date>` section.
3. Review and merge the changelog PR. This keeps the repository history and
   the published release consistent.

## Permissions and branch protection

- The workflow requires `contents: write` (configured in the workflow)
  so it can open PRs and create releases. If your organization restricts
  runner permissions, grant the necessary token rights.
- If `master` is protected (required checks, disallow force-push), the
  changelog PR ensures the workflow does not push directly to a protected
  branch.

## Troubleshooting

- "No changelog update" — the script looks for `## [<version>]` or
  `## [Unreleased]` in `CHANGELOG.md`. If those are missing it falls back
  to `git log` to build release notes.
- "PR not opened" — ensure `actions/checkout` ran with `fetch-depth: 0`
  and the runner has `GITHUB_TOKEN` available.
- "Cannot push or create PR" — check branch protection rules and token
  scopes; use the automation PR flow to respect protections.

## Admin tips

- If you prefer to include changelog in the tagged commit itself, create
  the changelog change and merge it first, then tag the merge commit.
- To test the generator locally:

```bash
node .github/scripts/generate-release-notes.js
```

This will print the generated body or write a `CHANGELOG.md` update in
place (use a disposable branch when testing).

## Where to look in the repo

- Workflow: `.github/workflows/release.yml`
- Release notes generator: `.github/scripts/generate-release-notes.js`
- Release automation PR action: `peter-evans/create-pull-request` in the
  workflow steps.

---

If you'd like, I can also add a short script to simulate the prepare job
locally and create the changelog branch automatically for testing.

## Local preview helper: `scripts/preview_changelog_pr.py`

A small helper script is included to reproduce the `prepare` job locally
and create a branch with the changelog update so you can inspect the PR
before pushing to GitHub.

- Location: `scripts/preview_changelog_pr.py`
- Purpose: run the generator for a specific tag, write `CHANGELOG.md`,
  create a local branch `changelog/<tag>` and commit the changelog change.

Usage (from repository root):

```bash
python scripts/preview_changelog_pr.py v0.3.0
```

Options:

- `--branch`: specify a different branch name (default `changelog/<tag>`)
- `--push`: push the created branch to `origin` (optional — the script
  does not push by default to avoid accidental uploads)

Notes and prerequisites:

- The helper invokes the release notes generator (`node .github/scripts/generate-release-notes.js`),
  so you need a working `node` executable available on your PATH.
- Run the script from the repository root. It will refuse to run if the
  working tree contains uncommitted changes other than `CHANGELOG.md`.
- The script is intentionally conservative: it creates a branch and a
  single commit for the changelog update; you can then `git push origin <branch>`
  and open a PR via the GitHub UI or use `gh` to create the PR.

Recommended workflow to preview a changelog PR locally:

```bash
# 1. Ensure clean working tree (or only CHANGELOG.md modified)
git status --porcelain

# 2. Run the helper for the tag you plan to publish
python scripts/preview_changelog_pr.py v0.3.0

# 3. Inspect the created branch and files
git checkout changelog/v0.3.0
git show --name-only

# 4. Push and open a PR when ready
git push origin changelog/v0.3.0
# then open a PR on GitHub from changelog/v0.3.0 -> master
```

If you'd like, I can add a short note in `CONTRIBUTING.md` with the same
instructions so maintainers see the workflow when making releases.
