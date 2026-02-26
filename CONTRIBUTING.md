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

- The repository uses an automated GitHub Actions workflow to produce
	release artifacts and to generate release notes. To keep the
	`CHANGELOG.md` in sync with releases the workflow will automatically
	generate a changelog section when a tag matching `v*` is pushed.

- Workflow behavior (maintainers and contributors):

	1. When a tag like `v0.3.0` is pushed, the `prepare` job runs and
		 executes `.github/scripts/generate-release-notes.js`. The script
		 extracts release notes from `CHANGELOG.md` (prefers `## [<version>]`,
		 then `## [Unreleased]`, then falls back to `git log`) and writes an
		 updated `CHANGELOG.md` that inserts a `## [<version>] — <date>`
		 section.

	2. The workflow then commits the changelog update to a new branch and
		 opens an automated pull request named `changelog/<tag>` targeting
		 `master`. This gives maintainers the opportunity to review and merge
		 the changelog change instead of allowing the workflow to push to the
		 protected branch directly.

	3. The build and release jobs create platform artifacts and a GitHub
		 Release using the generated release notes. The PR is independent of
		 the Release creation, so merging the changelog PR is recommended to
		 keep the repository history consistent with the published releases.

- Recommended maintainer steps when publishing a release:

	- Push an annotated tag from a local clone:

		```bash
		git tag -a v0.3.0 -m "Release v0.3.0"
		git push origin v0.3.0
		```

	- After pushing the tag, a PR `changelog/v0.3.0` will be opened
		automatically. Review and merge that PR to update `CHANGELOG.md` in
		the repository.

	- The release artifacts and the GitHub Release are created by the
		workflow; verify the release page and attached artifacts after the
		workflow completes.

- Notes and troubleshooting:

	- The workflow requires `contents: write` permissions (configured in
		the workflow) so that it can create PRs and releases; ensure the job
		runs with sufficient permissions in your organization.
	- If your default branch is not `master`, update the workflow files
		(`.github/workflows/release.yml` and the release script) to target
		the correct branch.
	- If you prefer the changelog to be included in the tagged commit
		itself, consider updating the release process to create tags only
		after the changelog PR is merged, or modify the workflow to re-tag
		(note: re-tagging rewrites history and is discouraged for public
		releases).

	### Local preview helper

	A small helper script is provided to reproduce the workflow's `prepare`
	job locally and create a branch containing the `CHANGELOG.md` update.

	- Location: `scripts/preview_changelog_pr.py`
	- Purpose: run the generator for a specific tag, write `CHANGELOG.md`,
	  create a local branch `changelog/<tag>` and commit the changelog change.

	Usage (from repository root):

	```bash
	python scripts/preview_changelog_pr.py v0.3.0
	```

	Options:

	- `--branch`: specify a different branch name (default `changelog/<tag>`)
	- `--push`: push the created branch to `origin` (the script does not
	  push by default to avoid accidental uploads)

	Notes:

	- The helper invokes the release notes generator (`node .github/scripts/generate-release-notes.js`),
	  so you need `node` available on your PATH.
	- The script refuses to run if the working tree contains uncommitted
	  changes other than `CHANGELOG.md` to avoid accidental commits.

	Recommended preview workflow:

	```bash
	# Ensure working tree is clean (or only CHANGELOG.md changed)
	git status --porcelain

	# Generate changelog update and create branch
	python scripts/preview_changelog_pr.py v0.3.0

	# Inspect the branch and commit
	git checkout changelog/v0.3.0
	git show --name-only

	# Push and open a PR when ready
	git push origin changelog/v0.3.0
	# then open a PR from changelog/v0.3.0 -> master
	```

	### Keeping documentation and changelog in sync

	All changes that add, alter or remove features must update the relevant
	documentation in the `docs/` folder and, when user-visible, the
	`CHANGELOG.md` file. A checklist to ensure docs stay in sync:

	- Add or update the corresponding `docs/` page(s) for the feature.
	- Update `CHANGELOG.md` under `## [Unreleased]` with a short entry.
	- Run the preview helper to verify the generated release section for a
	  given tag if you are preparing a release.
	- Run pre-commit and the test suite before opening a PR:

	```bash
	python -m pre_commit run --all-files
	pytest
	```

	- Include doc changes in the same PR as code changes when practical,
	  or reference the documentation PR in the issue/PR description.

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
