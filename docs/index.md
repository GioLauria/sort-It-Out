# SortItOut — Documentation

Welcome to the SortItOut documentation. This page provides a concise,
logical overview of the project, how to get started, and where to look for
further details.

## Overview

SortItOut benchmarks sorting algorithms on custom datasets and reports
average execution times. The project includes a small suite of sorting
implementations, timing utilities, and example tests.

## Goals

- Provide simple, readable implementations of common sorting algorithms.
- Offer timing helpers to measure algorithm performance on custom datasets.
- Make it easy to add new algorithms and datasets for benchmarking.

## Project layout

- `src/sort_it_out/` — package code (sorting algorithms, timing helpers).
- `tests/` — unit tests and test helpers.
- `docs/` — documentation (this file).

## Getting started

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install in editable mode and development requirements.

```powershell
pip install -e .
pip install -r requirements-dev.txt
```

4. (Optional but recommended) Install and enable pre-commit hooks.

```powershell
pip install pre-commit
pre-commit install
# Run all hooks once locally
pre-commit run --all-files
```

See the detailed per-platform instructions in `docs/pre-commit.md`.

3. Run tests.

```powershell
pytest
```

## Usage examples

Basic usage to sort and benchmark a small dataset:

```python
from sort_it_out import bubble_sort, merge_sort, compare_algorithms

data = [5, 3, 2, 4, 1]
print(bubble_sort(data))

algos = {
		"Bubble": bubble_sort,
		"Merge": merge_sort,
}
results = compare_algorithms(algos, data, repeat=5)
print(results)
```

CLI notes
---------

- The CLI supports reading input from a file or stdin and can write sorted
	results to a file using the `-o/--output` option. Example:

```bash
sortItOut -i data.txt -s Gnome -o sorted.txt
```

Versioning
----------

- The package version is produced by `setuptools_scm` from git tags when
	building/installing the package. At runtime the package prefers the
	generated `_version.py` and otherwise attempts to read the latest git tag.

## Algorithms included

- `bubble_sort` — simple O(n^2) comparison sort; useful for demonstrations.
- `quick_sort` — recursive quicksort with middle pivot; average O(n log n).
- `merge_sort` — classic divide-and-conquer stable sort; O(n log n).

See the full algorithm reference in the `algorithms` section:

- [Algorithms reference](algorithms/index.md)

Programmatic API
---------------

The package exposes a simple programmatic entrypoint `sort_it_out.run(argv)`
which runs the same CLI logic from Python. Example:

```python
import sort_it_out
sort_it_out.run(["-s", "Merge", "-i", "data.txt"])
```

Add additional algorithm modules under `src/sort_it_out/` and export them
from `src/sort_it_out/__init__.py` to make them available for benchmarking.

## Benchmarking and datasets

- Use `compare_algorithms` to benchmark multiple algorithms on the same
	dataset. It returns average execution time (seconds) per algorithm.
- For realistic benchmarking, provide larger datasets and control randomness
	(e.g., set a PRNG seed or load a deterministic dataset from a file).

## Tests

- Unit tests live in `tests/`. Run them with `pytest`.
- The test suite includes correctness checks and simple timing checks.

## Contributing

- Add new algorithms as modules in `src/sort_it_out/` with unit tests.
- Update documentation in `docs/` to describe new features.
- Follow the existing commit style and sign commits when pushing.

## License

This project is released under the MIT license (see the repository
`LICENSE` file).
