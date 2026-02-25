````markdown
## Quick Sort

Description
- Divide-and-conquer algorithm that selects a pivot and partitions the
  sequence into elements less than, equal to and greater than the pivot,
  then recursively sorts the partitions.

Complexity
- Worst-case: O(n^2) (rare, depends on pivot choice)
- Average-case: O(n log n)
- Best-case: O(n log n)

Space
- O(n) due to list copies in this implementation. In-place variants use
  O(log n) stack space on average.

Stable: No

Use
- General-purpose sorting with good average performance. Not stable in
  this implementation.

Example
```python
from sort_it_out import quick_sort
print(quick_sort([3,1,2]))
```

Implementation
- Provided as `quick_sort` in the `sort_it_out` package.

````
