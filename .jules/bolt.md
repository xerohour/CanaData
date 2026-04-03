
## 2026-04-03 - Pre-computing expensive string transformations for list comprehensions
**Learning:** In `CanaParse.py`, applying multiple filters to a dataset repeatedly executed expensive row transformations (`" ".join(row)`) inside a condition block, causing an O(num_filters * num_rows) performance bottleneck.
**Action:** Pre-compute and cache these transformations outside the filter loop (O(num_rows)) and pass the pre-computed values to the condition function using `zip()`. This significantly improves execution time (e.g. from 0.9s to 0.6s for 10000 rows x 10 filters).
