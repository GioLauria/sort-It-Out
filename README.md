
# SortItOut

SortItOut is a small educational project that implements many sorting
algorithms in pure Python and provides simple timing helpers to benchmark
them on custom datasets. Implementations live in the `sort_it_out` package
and are intentionally handwritten (no external sorting libraries are used).

Author: Giovanni Lauria <giovanni.lauria@gmail.com>

Getting started
--------------

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the package and developer dependencies:

```powershell
pip install -e .
pip install -r requirements-dev.txt
```

3. Run the tests:

```powershell
pytest
```

Pre-commit hooks (recommended)
------------------------------

This repository includes a `.pre-commit-config.yaml` to run formatters and
linters (Black, isort, flake8). To enable hooks:

```powershell
pip install pre-commit
python -m pre_commit install
python -m pre_commit run --all-files
```

See `docs/pre-commit.md` for platform-specific notes (Windows and Linux).

Quick usage
-----------

Import algorithms and timing helpers directly from the package:

```python
from sort_it_out import bubble_sort, merge_sort, compare_algorithms

data = [5, 3, 2, 4, 1]
print(bubble_sort(data))

algos = {
    "bubble": bubble_sort,
    "merge": merge_sort,
}
results = compare_algorithms(algos, data, repeat=5)
print(results)
```

For realistic benchmarks, prepare datasets of different sizes and
distributions (sorted, reverse-sorted, random, many duplicates) and use
`compare_algorithms` which returns average times in seconds.

Contributing and code of conduct
--------------------------------

- See `CONTRIBUTING.md` for development, testing and PR guidelines.
- See `CODE_OF_CONDUCT.md` for expected behaviour and reporting.

License
-------

This project is provided under the MIT license (see the `LICENSE` file).

Command-line usage
------------------

After installing the package (editable mode during development), a `sortItOut`
console command will be available. Basic usage:

```bash
# sort a file using merge sort (default)
sortItOut -i data.txt

# sort a file using quicksort
sortItOut -i data.txt -s quick

# print timing (average over 5 runs)
sortItOut -i data.txt -s quick --time -r 5

# read from stdin and use bubble sort
cat data.txt | sortItOut -s bubble
```

You can also explicitly pass `-` as the input filename to force reading from
stdin, e.g.:

```bash
cat data.txt | sortItOut -i - -s bubble
```

The `--sort` option accepts algorithm names: bubble, quick, merge, selection,
insertion, heap, shell, counting, radix, bucket, comb, cocktail, gnome.

Graphical interface
-------------------

You can run a simple graphical interface that accepts input, algorithm
selection and displays results using the `--gui` flag:

```bash
sortItOut --gui
```

The GUI uses Tkinter (part of the Python standard library) and requires no
additional dependencies.

Programmatic API
-----------------

You can invoke the tool programmatically from other Python code. Import the
package and call `run()` with an argv-like list to execute the CLI logic and
receive the CLI exit code. Example:

```python
import sort_it_out
exit_code = sort_it_out.run(["-s", "bubble", "-i", "data.txt"])
```
