# Contributing to SortItOut

Thanks for your interest in contributing to SortItOut. We welcome bug reports,
feature requests, and pull requests. This document explains how to contribute
effectively.

## How to file an issue

- Check existing issues for duplicates before opening a new one.
- Provide a clear title and a concise description of the problem or feature.
- Include steps to reproduce (for bugs), expected vs actual behavior, and any
	relevant logs or traceback.

## Development setup

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

or on Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```powershell
pip install -e .
pip install -r requirements-dev.txt
```

3. Install pre-commit hooks (recommended):

```powershell
pip install pre-commit
python -m pre_commit install
python -m pre_commit run --all-files
```

## Code style and tests

- Follow the existing style: `black` for formatting and `isort` for imports.
- Run the test suite before submitting a PR:

```powershell
pytest
```

## Making changes

- Create a new branch for your work (feature or bugfix).
- Keep changes small and focused; write tests for new behavior.
- Update the documentation in `docs/` as needed.

## Pull requests

- Open a PR against `master` with a clear title and description.
- Link related issues using "Fixes #<issue>" when appropriate.
- Maintain a clean commit history; squashing is acceptable at merge time.
- PRs should pass CI (tests and linters) before merging.

## Commit signing

- We prefer signed commits for maintainership verification. Configure GPG and
	sign commits with `git commit -S` if possible.

## Code of Conduct

All contributors must follow the project's `CODE_OF_CONDUCT.md`.

Thank you for contributing to SortItOut!

# Contributing

Thank you for considering contributing. Please follow the guidelines below.

- Fork the repo and create a feature branch.
- Follow the coding style (Black, isort, flake8).
- Run tests and linters before opening a PR.
- Include tests and update documentation for changes.
