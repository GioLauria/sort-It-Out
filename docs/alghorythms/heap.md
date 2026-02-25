## Heap Sort

Description
- Comparison-based algorithm that builds a heap and repeatedly extracts
  the maximum element to produce a sorted list.

Complexity
- Worst/Average/Best: O(n log n)

Space
- O(n) for this implementation (array copy). In-place heap algorithms can
  use O(1) extra space.

Stable: No

Use
- Good worst-case guarantees and memory-friendly in some in-place forms.

Example
```python
from sort_it_out import heap_sort
print(heap_sort([3,1,2]))
```

Implementation
- Provided as `heap_sort` in the `sort_it_out` package.
