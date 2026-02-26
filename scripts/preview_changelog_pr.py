#!/usr/bin/env python3
"""Create a local branch with the changelog update for a given tag.

Usage:
  python scripts/preview_changelog_pr.py v0.3.0

The script will run the release-notes generator with the provided tag
(environment `GITHUB_REF=refs/tags/<tag>`), write an updated
`CHANGELOG.md` (if applicable), create a branch `changelog/<tag>`, commit
the changelog change, and print instructions to push the branch and open
a PR. By default it does not push or create the PR.
"""

import argparse
import os
import subprocess
import sys


def run(cmd, check=True, capture=False, env=None):
    if capture:
        return subprocess.check_output(cmd, shell=True, env=env, text=True)
    else:
        return subprocess.check_call(cmd, shell=True, env=env)


def main():
    parser = argparse.ArgumentParser(description="Preview changelog PR branch")
    parser.add_argument("tag", help="Release tag to preview, e.g. v0.3.0")
    parser.add_argument(
        "--branch", help="Branch name to create (default: changelog/<tag>)"
    )
    parser.add_argument(
        "--push", action="store_true", help="Push the created branch to origin"
    )
    args = parser.parse_args()

    tag = args.tag
    branch = args.branch or f"changelog/{tag}"

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(repo_root)

    status = run("git status --porcelain", capture=True)
    if status.strip():
        entries = [entry for entry in status.splitlines() if entry.strip()]
        others = [
            entry
            for entry in entries
            if not entry.endswith(" CHANGELOG.md")
            and not entry.endswith("\tCHANGELOG.md")
        ]
        if others:
            print(
                "Error: working tree has uncommitted changes other than CHANGELOG.md."
            )
            print("Please commit or stash them before running this script.")
            sys.exit(1)

    print(f"Generating release notes for {tag} and updating CHANGELOG.md...")
    env = os.environ.copy()
    env["GITHUB_REF"] = f"refs/tags/{tag}"
    try:
        out = run(
            "node .github/scripts/generate-release-notes.js", capture=True, env=env
        )
        print(out)
    except subprocess.CalledProcessError as e:
        print("Error: running release-notes generator failed:", e)
        sys.exit(1)

    try:
        diff = run("git status --porcelain CHANGELOG.md", capture=True).strip()
    except subprocess.CalledProcessError:
        diff = ""

    if not diff:
        print("No CHANGELOG.md changes were produced by the generator.")
        print("If you expected a changelog update, check CHANGELOG.md manually.")
        sys.exit(0)

    try:
        existing = run(f"git rev-parse --verify {branch}", capture=True)
        if existing:
            print(f"Branch {branch} already exists locally.")
            print("Please remove it or use a different branch.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        pass

    print(f"Creating branch {branch} and committing CHANGELOG.md...")
    try:
        run(f"git checkout -b {branch}")
    except subprocess.CalledProcessError as e:
        print("Error creating branch:", e)
        sys.exit(1)

    try:
        run("git add CHANGELOG.md")
        run(f'git commit -m "chore(release): update CHANGELOG for {tag}"')
    except subprocess.CalledProcessError as e:
        print("No changelog commit was created (maybe no changes).", e)
        sys.exit(1)

    print("Branch created locally with changelog commit.")
    if args.push:
        try:
            print(f"Pushing branch {branch} to origin...")
            run(f"git push origin {branch}")
            print("Branch pushed. You can now open a PR on GitHub.")
        except subprocess.CalledProcessError as e:
            print("Failed to push branch:", e)
            sys.exit(1)
    else:
        print("To push the branch and open a PR, run:")
        print(f"  git push origin {branch}")
        print(f"Then open a PR from {branch} to master (or use gh / the GitHub UI).")

    print("Done.")


if __name__ == "__main__":
    main()
