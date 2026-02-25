# SortItOut

SortItOut provides small sorting helpers and example code for learning and
experimentation. The package is `sort_it_out` and the project is configured
for editable installs during development.

**Author:** Giovanni Lauria <giovanni.lauria@gmail.com>

Quick start:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install -r requirements-dev.txt
pytest
```

Usage
-
You can import and use the sorting helpers to benchmark algorithms on a
custom dataset. Example:

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

For benchmarking larger datasets, generate or load your dataset and pass it
to `compare_algorithms` which returns average times in seconds.

