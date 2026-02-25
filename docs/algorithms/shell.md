````markdown
## Shell Sort

Description
- An optimization of insertion sort that compares elements separated by a
  gap which decreases over time.

Complexity
- Worst-case: depends on gap sequence (commonly between O(n^2) and O(n^(3/2)))
- Average-case: typically better than insertion sort for medium-sized lists

Space
- O(n) when returning a copy; in-place variants use O(1).

Stable: No

Use
- Practical improvement over insertion sort for medium-sized arrays.

Example
```python
from sort_it_out import shell_sort
print(shell_sort([3,1,2]))
```

Implementation
- Provided as `shell_sort` in the `sort_it_out` package.

````
