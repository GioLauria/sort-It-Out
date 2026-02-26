#!/usr/bin/env python3
"""Apply branch protection to `master` using the GitHub CLI.

This script detects the remote `origin` owner/repo and calls `gh api`
to require status checks `CI` and `Python CI` and enforce admins.
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys


def detect_owner_repo() -> tuple[str, str]:
    out = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])  # may raise
    url = out.decode().strip()
    m = re.search(r"[:/](?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$", url)
    if not m:
        raise SystemExit(f"Unable to parse remote origin url: {url}")
    return m.group("owner"), m.group("repo")


def main() -> int:
    try:
        owner, repo = detect_owner_repo()
    except Exception as e:
        print("Error detecting repo owner/name:", e, file=sys.stderr)
        return 2

    protection_path = f"/repos/{owner}/{repo}/branches/master/protection"

    body = {
        "required_status_checks": {"strict": True, "contexts": ["CI", "Python CI"]},
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1,
        },
        # Restrict who can push directly to the branch. Set the repo owner
        # as the only allowed user to push.
        "restrictions": {"users": [owner], "teams": [], "apps": []},
    }

    # Write JSON body to a temp file and pass to `gh api --input` so types are preserved.
    import tempfile

    def _call_gh_with_body(body_obj: dict) -> tuple[int, str, str, str]:
        # write body to a temp file so JSON types are preserved
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", suffix=".json") as tf:
            tf.write(json.dumps(body_obj))
            path = tf.name
        cmd = ["gh", "api", "--method", "PUT", protection_path, "--input", path]
        print("Running:", " ".join(shlex.quote(c) for c in cmd))
        try:
            res = subprocess.run(cmd, check=False, capture_output=True, text=True)
            return res.returncode, res.stdout, res.stderr, path
        except FileNotFoundError:
            print("gh CLI not found. Install and authenticate with `gh auth login`.", file=sys.stderr)
            try:
                import os

                os.unlink(path)
            except Exception:
                pass
            return 3, "", "gh CLI not found", path

    rc, out, err, tf_path = _call_gh_with_body(body)

    # If this is a personal repository, the API rejects `restrictions.users`.
    # Detect that specific validation error and retry without restrictions.
    if rc != 0:
        combined = (out or "") + (err or "")
        if "Only organization repositories can have users and team restrictions" in combined:
            print("Personal repository detected — retrying without user/team restrictions")
            body["restrictions"] = None
            # remove previous temp file and retry
            try:
                import os

                os.unlink(tf_path)
            except Exception:
                pass
            rc2, out2, err2, tf_path2 = _call_gh_with_body(body)
            try:
                import os

                os.unlink(tf_path2)
            except Exception:
                pass
            if rc2 != 0:
                print("gh api failed on retry:", err2 or out2, file=sys.stderr)
                return rc2
            print("Branch protection applied for master on", owner + "/" + repo)
            return 0
        else:
            print("gh api failed:", err or out, file=sys.stderr)
            try:
                import os

                os.unlink(tf_path)
            except Exception:
                pass
            return rc
    # success on first try
    try:
        import os

        os.unlink(tf_path)
    except Exception:
        pass

    print("Branch protection applied for master on", owner + "/" + repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
