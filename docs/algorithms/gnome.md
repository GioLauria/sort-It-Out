````markdown
## Gnome Sort

Description
- Simple sorting algorithm similar to insertion sort that swaps elements
  to move them into order and steps backward when a swap occurs.

Complexity
- Worst/Average: O(n^2)
- Best: O(n)

Space
- O(n) for returned list; in-place variant uses O(1).

Stable: Yes

Use
- Educational and small lists.

Example
```python
from sort_it_out import gnome_sort
print(gnome_sort([3,1,2]))
```

Implementation
- Provided as `gnome_sort` in the `sort_it_out` package.

````
