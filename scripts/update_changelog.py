#!/usr/bin/env python3
"""Simple changelog updater used by CI to stamp Unreleased -> release.

Behavior:
- Reads CHANGELOG.md from repo root.
- Finds the first header matching "## [Unreleased]" and the following
  section until the next "## [" heading.
- Replaces that Unreleased section with a new release header using the
  provided tag (strip leading `v`) and today's date, leaving a fresh
  Unreleased section above it.

This script is intentionally small and has no external dependencies.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")


def load_changelog(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def save_changelog(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _version_key(v: str):
    parts = re.split(r"[.-]", v)
    key = []
    for p in parts:
        if p.isdigit():
            key.append(int(p))
        else:
            # keep non-numeric as lower-case string to compare
            key.append(p.lower())
    return tuple(key)


def make_release(changelog: str, version: str, date: str) -> str:
    # Locate Unreleased section
    m = re.search(r"^## \[Unreleased\]\s*$", changelog, flags=re.MULTILINE)
    if not m:
        # Prepend new release when Unreleased not found
        release_block = (
            f"## [{version}] - {date}\n\n- No changelog available for this release.\n\n"
        )
        return release_block + changelog

    intro = changelog[: m.start()]
    start = m.end()

    # Split the remainder into top-level sections starting with '## ['
    remainder = changelog[start:]
    sections = re.split(r"(?=^## \[)", remainder, flags=re.MULTILINE)

    # First section is the Unreleased content
    unreleased_section = sections[0].rstrip()
    other_sections = sections[1:]

    if not unreleased_section.strip():
        unreleased_section = "\n- No notable changes.\n"

    # Build the new release block from Unreleased
    release_block = f"## [{version}] - {date}\n\n" + unreleased_section + "\n\n"

    # Parse existing release sections into (version, block_text)
    releases = []
    for sec in other_sections:
        hdr = re.match(r"^## \[([^\]]+)\](?: - ([^\n]+))?\n", sec)
        if hdr:
            v = hdr.group(1)
            releases.append((v, sec.rstrip()))
        else:
            # keep orphan sections as-is with a low-priority key
            releases.append(("0.0.0", sec.rstrip()))

    # Add or replace the new release
    existing_versions = {v for v, _ in releases}
    if version in existing_versions:
        # replace existing entry
        releases = [
            (v, b) if v != version else (version, release_block.rstrip())
            for v, b in releases
        ]
    else:
        releases.append((version, release_block.rstrip()))

    # Sort releases by semantic version descending
    releases_sorted = sorted(releases, key=lambda vb: _version_key(vb[0]), reverse=True)

    # Reconstruct file: intro + Unreleased header + placeholder + sorted releases
    unreleased_placeholder = "## [Unreleased]\n\n- TODO: add unreleased changes\n\n"

    body = unreleased_placeholder
    for _, block in releases_sorted:
        body += block + "\n\n"

    return intro + body.rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    parser = argparse.ArgumentParser(description="Update CHANGELOG.md for a new tag")
    parser.add_argument(
        "--tag",
        help=(
            "Tag name (eg. v0.3.1 or 0.3.1). If omitted, uses "
            "GITHUB_REF_NAME env var."
        ),
    )
    args = parser.parse_args(argv)

    tag = args.tag or os.environ.get("GITHUB_REF_NAME") or os.environ.get("REF")
    if not tag:
        print("Error: tag not provided and GITHUB_REF_NAME not set", file=sys.stderr)
        return 2

    version = tag.lstrip("v")
    today = datetime.date.today().isoformat()

    content = load_changelog(CHANGELOG)
    new = make_release(content, version, today)
    if new == content:
        print("No changes made to CHANGELOG.md")
        return 0

    save_changelog(CHANGELOG, new)
    print(f"Updated CHANGELOG.md with release {version} ({today})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
