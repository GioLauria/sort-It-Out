#!/usr/bin/env python3
"""Check CHANGELOG.md contains entries under '## [Unreleased]'.

This script is intended to run in CI. It exits non-zero when files that
affect the code or docs were changed in the PR but `## [Unreleased]`
contains no list entries.
"""

from __future__ import annotations

import os
import re


def read_changed_files() -> list[str]:
    raw = os.environ.get("CHANGED_FILES", "")
    if not raw:
        return []
    return [line.strip() for line in raw.splitlines() if line.strip()]


def has_relevant_changes(changed: list[str]) -> bool:
    for p in changed:
        if (
            p.startswith("src/")
            or p.startswith("docs/")
            or p == "README.md"
            or p == "launcher.py"
        ):
            return True
    return False


def unreleased_has_entries(changelog_text: str) -> bool:
    m = re.search(r"^## \[Unreleased\]\s*$", changelog_text, re.MULTILINE)
    if not m:
        return False
    start = m.end()
    next_m = re.search(r"^## \[", changelog_text[start:], re.MULTILINE)
    section = (
        changelog_text[start : start + next_m.start()]
        if next_m
        else changelog_text[start:]
    )
    for line in section.splitlines():
        if line.strip().startswith("-"):
            return True
    return False


def main() -> int:
    changed = read_changed_files()
    if not has_relevant_changes(changed):
        print("No relevant code/docs changes detected; skipping changelog check.")
        return 0

    try:
        text = open("CHANGELOG.md", "r", encoding="utf8").read()
    except FileNotFoundError:
        print("CHANGELOG.md not found in repository root.")
        return 1

    ok = unreleased_has_entries(text)
    if ok:
        print("CHANGELOG.md: 'Unreleased' section contains entries.")
        return 0

    print("ERROR: CHANGELOG.md '## [Unreleased]' is empty but code/docs were changed.")
    print("Please add a short entry under '## [Unreleased]' describing the change.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
