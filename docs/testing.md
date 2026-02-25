# Testing

This document explains how the test suite for SortItOut is organized,
how to run the tests locally, what each test unit checks, and some
troubleshooting tips.

Where tests live
- `tests/test_sorts.py` — correctness and timing tests for the sorting
  algorithms and timing helpers.
- `tests/conftest.py` — test configuration, it ensures the repository's
  `src/` directory is on `sys.path` so `import sort_it_out` works during
  pytest runs.

How to run the tests locally
1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
```

2. Install the project in editable mode and developer dependencies:

```bash
pip install -e .
pip install -r requirements-dev.txt
```

3. (Recommended) Run pre-commit hooks once to ensure formatting and
   linting consistency before running tests:

```bash
python -m pre_commit install
python -m pre_commit run --all-files
```

4. Run pytest:

```bash
python -m pytest -q
```

What the tests cover
- `test_algorithms_sort_correctly` (parametrized):
  - Iterates over the implemented sorting functions (bubble, quick,
    merge, selection, insertion, heap, shell, counting, radix, comb,
    cocktail, gnome).
  - Generates a random list of integers and asserts that each algorithm's
    output equals Python's built-in `sorted()` result.
  - This verifies functional correctness across a variety of inputs.

- `test_time_sort_returns_float`:
  - Uses `time_sort` to run `merge_sort` and asserts that it returns a
    non-negative float. This ensures the timing helper runs without
    raising and produces a numeric result.

Notes about specific algorithms
- `counting_sort` and `radix_sort` expect integer inputs and will raise a
  `TypeError` if called with incompatible types (this is intentional and
  covered implicitly by tests which provide integers).
- `bucket_sort` expects floats in the range [0, 1). It is not included in
  the parametrized correctness test because its input constraints differ.

Randomness and reproducibility
- Tests use random input in `test_algorithms_sort_correctly`. This makes
  the test robust across many cases but non-deterministic. If you need
  deterministic runs (e.g., for CI debugging), you can set a fixed seed
  in the test or locally before running `pytest`:

```bash
python - <<'PY'
import random
random.seed(42)
import pytest
pytest.main()
PY
```

CI integration
- The repository includes a GitHub Actions workflow that runs `pytest` on
  push and pull requests. The CI job uses the same commands and should
  reflect the same status you see locally.

Troubleshooting
- If tests fail after code edits, run the formatters and linters
  locally (Black, isort, flake8) — pre-commit can run them all as shown
  above.
- If an algorithm raises `TypeError` for inputs that should be valid,
  inspect the implementation for input-type checks (particularly for
  `counting_sort`, `radix_sort`, and `bucket_sort`).
- To debug a failing algorithm deterministically, replace the random data
  generator in the test with a fixed dataset or print the failing input
  inside the test temporarily.

Extending tests
- Add a new test file under `tests/` for any new algorithms or
  utilities. Use parametrization (`pytest.mark.parametrize`) to avoid
  duplicating similar correctness checks across algorithms.
- If you add functionality that depends on external libraries or the
  GUI, consider adding optional tests that run only in appropriate CI
  environments or using mocking to avoid interactive windows.

Questions or additions
- If you'd like, I can: add deterministic seeds to tests, add a test for
  `bucket_sort`, or expand the CI workflow to include coverage or
  performance benchmarks. Tell me which one you prefer.
