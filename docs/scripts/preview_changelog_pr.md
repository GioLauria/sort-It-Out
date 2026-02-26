# preview_changelog_pr.py

Purpose
- Create a local branch with the changelog update for a given tag so you can inspect, push, and open a PR with the changelog changes.

Usage
- Example:

```bash
python scripts/preview_changelog_pr.py v0.3.0
```

Options
- `--branch`: specify branch name (default `changelog/<tag>`)
- `--push`: push the created branch to `origin` automatically

What it does
- Runs the release-notes generator (Node script) with `GITHUB_REF` set to the tag.
- If `CHANGELOG.md` changes, creates a branch `changelog/<tag>`, commits the changelog, and prints instructions to push/open a PR (or pushes if `--push` provided).

Notes
- The working tree must be clean except for changes to `CHANGELOG.md` (script will error if there are other uncommitted changes).
- This script depends on the repository's Node-based release-notes generator (`.github/scripts/generate-release-notes.js`).
