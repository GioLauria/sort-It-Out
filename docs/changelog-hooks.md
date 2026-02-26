# Local Changelog Hook

This project uses a local Git pre-push hook that updates `CHANGELOG.md`
automatically when you push tags from your machine. The hook runs
`scripts/update_changelog.py` for each pushed tag and, if the changelog is
modified, stages and commits the updated `CHANGELOG.md` locally and pushes the
branch so the changelog change is present on the remote before the tag.

Purpose
- Keep `CHANGELOG.md` consistent with tag releases without requiring manual
  edits or a remote-only GitHub Action.

Install (per-machine)

Run this once on each machine that will push tags:

```powershell
python scripts/install_hooks.py
```

How it works
- The hook is implemented in `scripts/local_pre_push.py` and installed to
  `.git/hooks/pre-push` by the installer.
- On a `git push` the hook reads the refs being pushed. For each pushed tag it:
  - runs `python scripts/update_changelog.py --tag <tag>`
  - if `CHANGELOG.md` is modified, stages and commits it with message
    `chore(release): update CHANGELOG for <tag>`
  - pushes `origin HEAD` so the changelog commit is available remotely before
    the tag is pushed.

Notes & caveats
- Hooks are local to the repository clone — other machines will not run the
  hook unless they install it. Add a note in your developer docs so other
  maintainers run the installer.
- To bypass hooks (for automated pushes or CI) use `git push --no-verify`.
- The previous GitHub Actions workflow that updated the changelog on tag
  pushes was removed from this repository; the local hook replaces that
  behavior.

Testing locally

1. Install the hook (see Install above).
2. Create and push an annotated tag:

```powershell
git tag -a v0.3.3 -m "Release v0.3.3"
git push origin v0.3.3
```

3. The pre-push hook will run: if it updates `CHANGELOG.md` it'll commit and
   push the branch automatically before the tag arrives on the remote.

Uninstall

Remove the hook script:

```powershell
rm .git/hooks/pre-push
```

Questions or changes
- If you prefer a repository-level enforcement (so all machines behave the
  same) we can reintroduce a workflow that runs on tag pushes instead, but
  this was intentionally removed to avoid duplicate updates and to keep
  changelog edits local and reviewable.
