## Radix Sort

Description
- Non-comparison integer sorting algorithm that processes individual digits
  (or groups of bits) and sorts by digit using a stable subroutine.

Complexity
- Typical: O(d * (n + b)) where d is number of digits and b is base (constant)

Space
- O(n + b) for buckets; this implementation returns a new list.

Stable: Yes (depends on stable digit-sorting step)

Use
- Efficient for integers when the number of digits is small relative to n.

Constraints
- Requires integer inputs; implementation handles negatives by offsetting.

Example
```python
from sort_it_out import radix_sort
print(radix_sort([3,1,2]))
```

Implementation
- Provided as `radix_sort` in the `sort_it_out` package.
