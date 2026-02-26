#!/usr/bin/env python3
"""Local pre-push hook logic.

This script is intended to be invoked from .git/hooks/pre-push. It reads the
refs being pushed from stdin and, for each pushed tag, runs
`scripts/update_changelog.py --tag <tag>` to update `CHANGELOG.md`. If the
file changes it commits the update locally and pushes the branch HEAD to
`origin` so the changelog update is included on the remote before the tag is
pushed.

The script avoids recursion by checking the environment variable
`LOCAL_PRE_PUSH_RUNNING`.
"""
from __future__ import annotations

import os
import subprocess
import sys
from typing import Iterable

ROOT = os.path.dirname(os.path.dirname(__file__))


def read_refs(stdin: Iterable[str]) -> list[tuple[str, str, str, str]]:
    # Each line: <local ref> <local sha> <remote ref> <remote sha>
    out = []
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 4:
            continue
        out.append((parts[0], parts[1], parts[2], parts[3]))
    return out


def run_update_for_tag(tag: str) -> bool:
    # Run the updater script for the given tag. Returns True if CHANGELOG.md
    # was modified.
    python = sys.executable or "python"
    try:
        subprocess.check_call(
            [
                python,
                os.path.join(ROOT, "scripts", "update_changelog.py"),
                "--tag",
                tag,
            ],
            cwd=ROOT,
        )
    except subprocess.CalledProcessError:
        return False

    # Check if CHANGELOG.md has unstaged changes
    st = (
        subprocess.check_output(
            ["git", "status", "--porcelain", "--", "CHANGELOG.md"], cwd=ROOT
        )
        .decode()
        .strip()
    )
    return bool(st)


def main() -> int:
    # Prevent recursion when this script performs its own git push
    if os.environ.get("LOCAL_PRE_PUSH_RUNNING"):
        return 0

    # Run the test suite before allowing a push to proceed. This blocks
    # pushes when tests fail to help keep remote branches green. Set
    # `SKIP_PRE_PUSH_TESTS=1` in the environment to opt out (useful for
    # emergency or very large test suites).
    if not os.environ.get("SKIP_PRE_PUSH_TESTS"):
        python = sys.executable or "python"
        try:
            subprocess.check_call([python, "-m", "pytest", "-q"], cwd=ROOT)
        except subprocess.CalledProcessError:
            print("Pre-push: tests failed. Aborting push.", file=sys.stderr)
            return 1

    refs = read_refs(sys.stdin)
    tags = []
    for local_ref, local_sha, remote_ref, remote_sha in refs:
        if remote_ref.startswith("refs/tags/"):
            tag = remote_ref.split("/", 2)[2]
            tags.append(tag)

    if not tags:
        return 0

    changed = False
    for tag in tags:
        ok = run_update_for_tag(tag)
        if ok:
            # stage and commit the changelog update
            subprocess.check_call(["git", "add", "CHANGELOG.md"], cwd=ROOT)
            try:
                subprocess.check_call(
                    [
                        "git",
                        "commit",
                        "-m",
                        f"chore(release): update CHANGELOG for {tag}",
                    ],
                    cwd=ROOT,
                )
            except subprocess.CalledProcessError:
                # nothing to commit
                pass
            changed = True

    if changed:
        # Push the branch HEAD so the changelog commit is available remotely
        env = os.environ.copy()
        env["LOCAL_PRE_PUSH_RUNNING"] = "1"
        subprocess.check_call(["git", "push", "origin", "HEAD"], cwd=ROOT, env=env)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
