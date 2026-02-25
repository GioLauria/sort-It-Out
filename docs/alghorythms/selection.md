## Selection Sort

Description
- Repeatedly selects the minimum (or maximum) element and moves it to the
  sorted portion of the list.

Complexity
- Worst/Average/Best: O(n^2)

Space
- O(n) when returning a new list; in-place uses O(1).

Stable: No (unless implemented carefully)

Use
- Educational; tiny lists.

Example
```python
from sort_it_out import selection_sort
print(selection_sort([3,1,2]))
```

Implementation
- Provided as `selection_sort` in the `sort_it_out` package.
