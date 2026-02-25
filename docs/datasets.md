# Dataset Formats and Guidelines

This page explains recommended dataset shapes and conventions for benchmarking.

Recommended dataset formats

- Plain lists of comparable values (e.g., `List[int]`, `List[float]`, or `List[str]`).
- Files with values per line (one value per line) which can be loaded and converted to a list.

Guidelines

- Use deterministic datasets for repeatable benchmarks. If randomness is used, fix the PRNG seed.
- Benchmark on multiple sizes and varied distributions:
  - Sorted ascending
  - Sorted descending
  - Random uniform
  - Few unique values (many duplicates)
- Avoid measuring wall-clock variance by running each algorithm multiple times and using the average returned by `compare_algorithms`.

Loading datasets

Example to load a newline-separated integers file:

```python
def load_ints(path: str) -> list[int]:
    with open(path, "r", encoding="utf-8") as fh:
        return [int(line.strip()) for line in fh if line.strip()]

data = load_ints("data/my_dataset.txt")
```
