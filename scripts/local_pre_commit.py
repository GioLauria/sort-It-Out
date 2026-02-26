#!/usr/bin/env python3
"""Run tests before committing. Exit non-zero to block the commit on failure.

This script is intended to be invoked from a git `pre-commit` hook shim.
It runs the project's test suite with the active Python executable so it
honors the virtualenv (`sys.executable`).

Set the environment variable `SKIP_PRE_COMMIT_TESTS=1` to bypass locally.
"""
from __future__ import annotations

import os
import subprocess
import sys


def main() -> int:
    if os.environ.get("SKIP_PRE_COMMIT_TESTS"):
        print("SKIP_PRE_COMMIT_TESTS set — skipping tests")
        return 0

    cmd = [sys.executable, "-m", "pytest", "-q"]
    print("Running tests before commit:", " ".join(cmd))
    try:
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print("Tests failed — aborting commit", file=sys.stderr)
            return res.returncode
        print("All tests passed — continuing commit")
        return 0
    except FileNotFoundError:
        print(
            "pytest not found in this environment. Install dev requirements or set SKIP_PRE_COMMIT_TESTS=1 to bypass.",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
