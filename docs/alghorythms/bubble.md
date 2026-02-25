## Bubble Sort

Description
- Simple comparison-based sorting algorithm that repeatedly steps through
  the list, compares adjacent items and swaps them if they are in the
  wrong order.

Complexity
- Worst-case: O(n^2)
- Average-case: O(n^2)
- Best-case: O(n) when the list is already sorted (with early exit)

Space
- O(n) additional when implemented as returning a new list (this package
  copies input). In-place variant uses O(1) extra space.

Stable: Yes (when implemented as swapping adjacent equal elements carefully)

Use
- Educational, tiny lists, nearly-sorted inputs (with the early-exit
  optimization).

Example
```python
from sort_it_out import bubble_sort
print(bubble_sort([3,1,2]))
```

Implementation
- Provided as `bubble_sort` in the `sort_it_out` package.
