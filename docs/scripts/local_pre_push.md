# local_pre_push.py

Purpose
- Hook logic executed by the `pre-push` git hook shim. When tags are pushed, it runs the changelog updater for each tag, commits any `CHANGELOG.md` changes, and pushes the branch head so the changelog update is available remotely before the tag.

Behavior
- Reads pushed refs from stdin (git provides lines describing refs being pushed).
- For each pushed tag, runs `python scripts/update_changelog.py --tag <tag>`.
- If `CHANGELOG.md` changed, stages and commits it and pushes `origin HEAD` to make the changelog commit available on the remote.

Notes
- Prevents recursion via the `LOCAL_PRE_PUSH_RUNNING` environment variable.
- Intended to be run via `.git/hooks/pre-push` shim installed by `scripts/install_hooks.py`.

Usage
- No direct arguments; invoked automatically by git when the pre-push hook runs. For local testing you can run it manually (it expects git refs on stdin). Example (test):

```bash
echo "refs/heads/master 012345 refs/tags/v0.0.0 000000" | python scripts/local_pre_push.py
```
