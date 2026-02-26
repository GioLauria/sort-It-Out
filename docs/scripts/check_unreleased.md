# check_unreleased.py

Purpose
- Ensure the `CHANGELOG.md` file contains entries under the `## [Unreleased]` section when code or docs were changed.

When to run
- Intended for CI (pull-request) checks. The script reads the `CHANGED_FILES` environment variable and exits non-zero when relevant files changed but no `Unreleased` entries exist.

Usage
- In CI set `CHANGED_FILES` (one path per line) and run:

```bash
python scripts/check_unreleased.py
```

Notes
- Returns `0` when either there are no relevant changes or `Unreleased` contains entries.
- Returns non-zero if `CHANGELOG.md` is missing or `Unreleased` is empty while code/docs changed.
