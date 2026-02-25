## Insertion Sort

Description
- Builds the sorted list one element at a time by inserting elements into
  their correct position.

Complexity
- Worst-case: O(n^2)
- Average-case: O(n^2)
- Best-case: O(n)

Space
- O(n) if returning a copy; in-place variant uses O(1).

Stable: Yes

Use
- Small lists and nearly-sorted inputs.

Example
```python
from sort_it_out import insertion_sort
print(insertion_sort([3,1,2]))
```

Implementation
- Provided as `insertion_sort` in the `sort_it_out` package.
