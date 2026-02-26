#!/usr/bin/env python3
"""Run the changelog updater for all git tags (newest -> oldest)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tags_list() -> list[str]:
    out = subprocess.check_output(["git", "tag", "--sort=-v:refname"], cwd=ROOT)
    return [t.strip() for t in out.decode().splitlines() if t.strip()]


def main() -> int:
    tags = tags_list()
    if not tags:
        print("No tags found; nothing to do.")
        return 0

    for t in tags:
        print("Updating changelog for", t)
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "update_changelog.py"), "--tag", t],
            check=True,
            cwd=ROOT,
        )

    print("All tags processed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
