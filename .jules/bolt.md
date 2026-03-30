
## 2026-03-30 - Precompute Expensive Row Transformations
**Learning:** In list comprehensions that evaluate multiple conditions (like applying multiple filters to a dataset), repeatedly executing expensive row transformations (e.g. `" ".join([str(x) for x in row]).lower()`) inside the condition causes severe performance bottlenecks (O(num_filters * num_rows)).
**Action:** Pre-compute and cache these transformations outside the filter loop (O(num_rows)) to significantly improve execution time, and pass the pre-computed value to the condition function using zip.
