```markdown
# API Reference

This page documents the public API of the `sort_it_out` package.

## Module: `sort_it_out.sorts`

Public functions:

- `bubble_sort(data: Iterable) -> List` — Simple comparison-based sort. Returns a new list containing the sorted items.
- `quick_sort(data: Iterable) -> List` — Recursive quicksort implementation. Returns a new sorted list.
- `merge_sort(data: Iterable) -> List` — Stable merge sort. Returns a new sorted list.
- `time_sort(algorithm: Callable[[Iterable], List], data: Iterable, repeat: int = 3) -> float` — Run `algorithm` on `data` `repeat` times and return the average execution time in seconds.
- `compare_algorithms(algorithms: Dict[str, Callable[[Iterable], List]], data: Iterable, repeat: int = 3) -> Dict[str, float]` — Run timing for each algorithm and return mapping `name -> avg_seconds`.
- `selection_sort`, `insertion_sort`, `heap_sort`, `shell_sort`, `counting_sort`, `radix_sort`, `bucket_sort`, `comb_sort`, `cocktail_sort`, `gnome_sort` — Additional handwritten implementations included in the package. See `src/sort_it_out/sorts.py` for details.

## Module: `sort_it_out` (package-level)

- `__version__` — Package version. When installed from source the project uses `setuptools_scm` to generate `src/sort_it_out/_version.py` from git tags; at runtime the package prefers the generated value and falls back to the latest git tag or `0.0.0` when necessary.
- `run(argv: Optional[List[str]] = None) -> int` — Programmatic entrypoint that runs the same CLI logic used by the `sortItOut` console script. Callers can pass an argv-like list (e.g. `['-s','merge','-i','data.txt']`) and receive an integer exit code.

Notes:

- All sorting functions return new lists and do not modify the input.
- For accurate timing, provide immutable data copies or ensure the timing helper recreates the dataset between runs.

Implementation note:

- All algorithms in this project are implemented in pure Python within the
  `sort_it_out` package. We do not use external sorting libraries or call
  third-party implementations. The built-in `sorted()` is not used in the
  algorithm implementations for the core sorting logic — the sorting
  algorithms themselves are handwritten for study and benchmarking purposes.

```
