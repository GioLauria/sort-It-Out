#!/usr/bin/env python3
"""Install git hooks for this repository (writes to .git/hooks).

Run this locally once to enable the pre-push behavior that updates the
`CHANGELOG.md` when tags are pushed.
"""
from __future__ import annotations

import os
import stat
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
HOOKS_DIR = os.path.join(ROOT, ".git", "hooks")
PRE_PUSH_SRC = os.path.join(ROOT, "scripts", "local_pre_push.py")
PRE_PUSH_DEST = os.path.join(HOOKS_DIR, "pre-push")
PRE_COMMIT_SRC = os.path.join(ROOT, "scripts", "local_pre_commit.py")
PRE_COMMIT_DEST = os.path.join(HOOKS_DIR, "pre-commit")


def install() -> None:
    if not os.path.isdir(HOOKS_DIR):
        print(
            "Error: .git/hooks directory not found. Are you in a git repo?",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # Write the hook file; include a small shim to run the script with python
    shim = (
        "#!/usr/bin/env python3\n"
        "import runpy, os, sys\n"
        "runpy.run_path(\n"
        "    os.path.join(\n"
        "        os.path.dirname(__file__),\n"
        "        '..', '..', 'scripts', 'local_pre_push.py'\n"
        "    ),\n"
        "    run_name='__main__'\n"
        ")\n"
    )

    with open(PRE_PUSH_DEST, "w", encoding="utf-8") as fh:
        fh.write(shim)

    # make executable
    st = os.stat(PRE_PUSH_DEST)
    os.chmod(PRE_PUSH_DEST, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("Installed pre-push hook to .git/hooks/pre-push")
    # Install pre-commit hook shim
    shim_commit = (
        "#!/usr/bin/env python3\n"
        "import runpy, os, sys\n"
        "runpy.run_path(\n"
        "    os.path.join(\n"
        "        os.path.dirname(__file__),\n"
        "        '..', '..', 'scripts', 'local_pre_commit.py'\n"
        "    ),\n"
        "    run_name='__main__'\n"
        ")\n"
    )

    with open(PRE_COMMIT_DEST, "w", encoding="utf-8") as fh:
        fh.write(shim_commit)
    st = os.stat(PRE_COMMIT_DEST)
    os.chmod(PRE_COMMIT_DEST, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("Installed pre-commit hook to .git/hooks/pre-commit")
    # Gentle reminder for other developers after cloning
    print(
        (
            "Reminder: run 'python scripts/install_hooks.py' after cloning "
            "to enable the pre-push hook."
        )
    )


if __name__ == "__main__":
    install()
