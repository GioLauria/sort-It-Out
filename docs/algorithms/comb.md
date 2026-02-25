````markdown
## Comb Sort

Description
- Improvement over bubble sort that eliminates turtles (small values at the
  end) by using a shrinking gap between compared elements.

Complexity
- Average-case: typically better than bubble sort; worst-case O(n^2)

Space
- O(n) for returned list; in-place variants use O(1).

Stable: No

Use
- Educational and small-to-medium lists where simple optimizations help.

Example
```python
from sort_it_out import comb_sort
print(comb_sort([3,1,2]))
```

Implementation
- Provided as `comb_sort` in the `sort_it_out` package.

````
