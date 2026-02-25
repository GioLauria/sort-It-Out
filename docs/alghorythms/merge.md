## Merge Sort

Description
- Stable divide-and-conquer algorithm that splits the list, sorts each
  half and merges the sorted halves.

Complexity
- Worst-case: O(n log n)
- Average-case: O(n log n)
- Best-case: O(n log n)

Space
- O(n) additional space for merging (this implementation builds new lists).

Stable: Yes

Use
- Reliable general-purpose sorting where stability is desired.

Example
```python
from sort_it_out import merge_sort
print(merge_sort([3,1,2]))
```

Implementation
- Provided as `merge_sort` in the `sort_it_out` package.
