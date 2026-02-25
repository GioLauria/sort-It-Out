````markdown
## Cocktail Sort

Description
- Bidirectional variant of bubble sort that traverses the list in both
  directions alternately.

Complexity
- Worst/Average: O(n^2)
- Best: O(n) with early-exit optimization

Space
- O(n) for returned list; in-place variant uses O(1).

Stable: Yes (when swapping preserves order of equals)

Use
- Small lists and cases where bidirectional passes reduce swaps.

Example
```python
from sort_it_out import cocktail_sort
print(cocktail_sort([3,1,2]))
```

Implementation
- Provided as `cocktail_sort` in the `sort_it_out` package.

````
