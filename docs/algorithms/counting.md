````markdown
## Counting Sort

Description
- Non-comparison integer sorting algorithm that counts occurrences of each
  value and reconstructs the sorted list.

Complexity
- Worst/Average/Best: O(n + k) where k is the range of input values

Space
- O(k) additional space for the counts; this implementation returns a new list.

Stable: Yes (when implemented preserving order of equal keys)

Use
- Very efficient when the range `k` is not much larger than `n` and inputs
  are integers.

Constraints
- Requires integer inputs.

Example
```python
from sort_it_out import counting_sort
print(counting_sort([3,1,2]))
```

Implementation
- Provided as `counting_sort` in the `sort_it_out` package and will raise
  `TypeError` if non-integer inputs are provided.

````
