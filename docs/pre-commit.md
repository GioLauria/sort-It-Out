# Pre-commit hook setup (Windows and Linux)

This document explains how to enable and run the project's pre-commit hooks on
both Windows and Linux. The repository contains a `.pre-commit-config.yaml` at
the project root that configures hooks such as `black`, `isort`, and `flake8`.

Overview steps (both platforms):

1. Install `pre-commit` in the environment you use for development.
2. Install the git hooks into your repository with `pre-commit install`.
3. Optionally run `pre-commit run --all-files` to apply hooks across the repo.

Windows (PowerShell) — recommended

Open PowerShell and run:

```powershell
# create/activate your venv (optional but recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install pre-commit (user/site packages if you prefer)
pip install --upgrade pip
pip install pre-commit

# Install hooks into .git/hooks
python -m pre_commit install

# Run hooks across all files once
python -m pre_commit run --all-files
```

Notes for Windows users:
- If `pre-commit` was installed but `pre-commit` is not recognized as a command,
  use `python -m pre_commit ...` as shown above. This avoids PATH issues.
- The `python -m pre_commit install` command registers the hook scripts in
  `.git/hooks/pre-commit` for the current repository.

Linux / macOS (bash)

Open a terminal and run:

```bash
# create/activate a venv (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install pre-commit

# Install hooks into .git/hooks
python -m pre_commit install

# Run hooks across all files once
python -m pre_commit run --all-files
```

Advanced notes

- To skip hooks for a single commit, use `git commit --no-verify`.
- To run a single hook manually, use `pre-commit run <hook-id> --all-files`.
- If hooks modify files (e.g., `black` or `isort`), re-run `git add` and re-commit.
- The `.pre-commit-config.yaml` in the project root controls which hooks run.

If you prefer not to use pre-commit hooks, remove the file at the project root
(`.pre-commit-config.yaml`) and commit that change. Otherwise the hooks are
recommended to keep the codebase consistent and to catch simple issues early.
