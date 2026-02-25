# API Reference

This page documents the public API of the `sort_it_out` package.

## Module: `sort_it_out.sorts`

Public functions:

- `bubble_sort(data: Iterable) -> List` — Simple comparison-based sort. Returns a new list containing the sorted items.
- `quick_sort(data: Iterable) -> List` — Recursive quicksort implementation. Returns a new sorted list.
- `merge_sort(data: Iterable) -> List` — Stable merge sort. Returns a new sorted list.
- `time_sort(algorithm: Callable[[Iterable], List], data: Iterable, repeat: int = 3) -> float` — Run `algorithm` on `data` `repeat` times and return the average execution time in seconds.
- `compare_algorithms(algorithms: Dict[str, Callable[[Iterable], List]], data: Iterable, repeat: int = 3) -> Dict[str, float]` — Run timing for each algorithm and return mapping `name -> avg_seconds`.

Notes:

- All sorting functions return new lists and do not modify the input.
- For accurate timing, provide immutable data copies or ensure the timing helper recreates the dataset between runs.
