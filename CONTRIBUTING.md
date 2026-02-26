# Contributing to SortItOut

Thanks for your interest in contributing to SortItOut. We welcome bug reports,
feature requests, and pull requests. This document explains how to contribute
effectively.

## How to file an issue

- Check existing issues for duplicates before opening a new one.
- Provide a clear title and a concise description of the problem or feature.
- Include steps to reproduce (for bugs), expected vs actual behavior, and any
	relevant logs or traceback.

## Development setup

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

or on Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```powershell
pip install -e .
pip install -r requirements-dev.txt
```

3. Install pre-commit hooks (recommended):

```powershell
pip install pre-commit
python -m pre_commit install
python -m pre_commit run --all-files
```

## Code style and tests

- Follow the existing style: `black` for formatting and `isort` for imports.
- Run the test suite before submitting a PR:

```powershell
pytest
```

## Making changes

- Create a new branch for your work (feature or bugfix).
- Keep changes small and focused; write tests for new behavior.
- Update the documentation in `docs/` as needed.

## Pull requests

- Open a PR against `master` with a clear title and description.
- Link related issues using "Fixes #<issue>" when appropriate.
- Maintain a clean commit history; squashing is acceptable at merge time.
- PRs should pass CI (tests and linters) before merging.

## Releases and changelog

The project uses a local pre-push hook to keep `CHANGELOG.md` synchronized
with tag releases. Maintainers and contributors must follow these steps to
ensure the changelog is updated and published alongside tags.

### Install the local hook (per machine)

Run this once for every clone where you will push tags:

```powershell
python scripts/install_hooks.py
```

This installs a `pre-push` hook in `.git/hooks/pre-push` that:

- detects any tags being pushed;
- runs `python scripts/update_changelog.py --tag <tag>` for each pushed tag;
- if `CHANGELOG.md` was modified, stages and commits it locally with message
  `chore(release): update CHANGELOG for <tag>` and pushes `origin HEAD` so the
  changelog commit reaches the remote before the tag.

Note: hooks are local to the clone. Make sure all maintainers install the
hook; otherwise tag pushes from clones without the hook will not update the
changelog automatically.

### Tagging and pushing a release (maintainer workflow)

1. Ensure your working tree is clean (except uncommitted changes to
   `CHANGELOG.md` if you are editing it manually):

```powershell
git status --porcelain
```

2. Create an annotated tag locally (replace `vX.Y.Z`):

```powershell
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

3. Push the tag to remote:

```powershell
git push origin vX.Y.Z
```

The `pre-push` hook will run when the tag push occurs. If the hook updates
`CHANGELOG.md`, it will commit and push the changelog update (`origin HEAD`) so
the changelog edit arrives on the remote before the tag.

### Bypassing the hook

Automation or CI systems may need to bypass hooks; use `--no-verify` to skip
hooks when pushing:

```powershell
git push --no-verify origin vX.Y.Z
```

Use this carefully; skipping hooks means the changelog will not be updated
automatically by the local process.

### Testing the process locally

1. Install the hook:

```powershell
python scripts/install_hooks.py
```

2. Create a tag and push it (see Tagging and pushing a release). Observe the
   hook's output; if `CHANGELOG.md` was updated it will be committed and the
   branch pushed before the tag arrives.

3. Verify on GitHub that both the changelog commit and the tag are present.

### Onboarding new maintainers

Add the following checklist to your onboarding notes or `CONTRIBUTING.md`
overview so new maintainers know to install the hook:

- Run `python scripts/install_hooks.py` after cloning the repository.
- Use annotated tags (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`).
- Push tags normally (`git push origin vX.Y.Z`) — the local hook will handle
  changelog updates and push the changelog commit automatically.

### If you prefer a repo-level workflow

If you want changelog updates to be performed centrally (via GitHub Actions)
instead of locally, we can reintroduce the workflow that runs on tag pushes
and commits the changelog on the remote. That approach ensures consistent
behavior across all machines but requires careful coordination to avoid
duplicate commits when both local hooks and the workflow run.


## Commit signing

- We prefer signed commits for maintainership verification. Configure GPG and
	sign commits with `git commit -S` if possible.

## Code of Conduct

All contributors must follow the project's `CODE_OF_CONDUCT.md`.

Thank you for contributing to SortItOut!

# Contributing

Thank you for considering contributing. Please follow the guidelines below.

- Fork the repo and create a feature branch.
- Follow the coding style (Black, isort, flake8).
- Run tests and linters before opening a PR.
- Include tests and update documentation for changes.
