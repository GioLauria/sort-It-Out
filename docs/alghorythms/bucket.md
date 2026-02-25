## Bucket Sort

Description
- Distributes elements into a number of buckets, sorts each bucket, and
  concatenates the results.

Complexity
- Average-case: O(n + k) where k is number of buckets and depends on
  distribution

Space
- O(n + k) additional space for buckets

Stable: Depends on bucket-sorting subroutine

Use
- Effective when input is uniformly distributed over a known range.

Constraints
- This implementation expects floats in [0, 1).

Example
```python
from sort_it_out import bucket_sort
print(bucket_sort([0.3, 0.1, 0.2]))
```

Implementation
- Provided as `bucket_sort` in the `sort_it_out` package and will raise
  `TypeError` if inputs are not floats in the expected range.
