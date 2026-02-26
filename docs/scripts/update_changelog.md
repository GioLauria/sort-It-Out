# update_changelog.py

Purpose
- Small, dependency-free script to stamp the current `Unreleased` section in `CHANGELOG.md` into a new release header for a provided tag.

Behavior
- Reads `CHANGELOG.md` from the repository root, locates the `## [Unreleased]` section, and creates a release block for the given tag and today's date. Leaves a fresh `Unreleased` placeholder.
- Attempts to build structured release notes by scanning git commits for Conventional Commit prefixes and grouping them into Keep-a-Changelog sections.

Usage

```bash
python scripts/update_changelog.py --tag v0.3.1
```

Notes
- If `--tag` is omitted the script looks for `GITHUB_REF_NAME` or `REF` environment variables (useful in CI).
- The script writes changes to `CHANGELOG.md` when updates are produced and returns a non-zero exit code for missing tag or errors.
