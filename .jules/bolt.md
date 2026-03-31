## 2024-05-15 - Caching expensive row transformations outside filter loop in list comprehensions
**Learning:** In list comprehensions that evaluate multiple conditions (e.g., applying multiple filters to a dataset), repeatedly executing expensive row transformations (like " ".join(row)) inside the condition causes severe performance bottlenecks (O(num_filters * num_rows)).
**Action:** Pre-compute and cache these transformations outside the filter loop (O(num_rows)) to significantly improve execution time, and pass the pre-computed values to the condition function using zip().
