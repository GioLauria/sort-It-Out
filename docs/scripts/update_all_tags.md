# update_all_tags.py

Purpose
- Run the changelog updater for every git tag in the repository (newest → oldest).

Usage

```bash
python scripts/update_all_tags.py
```

What it does
- Enumerates tags using `git tag --sort=-v:refname` and runs `scripts/update_changelog.py --tag <tag>` for each tag.

Notes
- Intended for offline or administrative updates to regenerate changelog entries across tags.
- Requires `git` available in PATH and to be run from the repository root (script sets cwd accordingly).
