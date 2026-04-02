## 2026-04-02 - String Join Optimization in Filter Loops
**Learning:** In list comprehensions evaluating multiple conditions, executing expensive row transformations (like `" ".join(row)`) inside the condition causes severe performance bottlenecks `O(num_filters * num_rows)`.
**Action:** Pre-compute and cache these string transformations outside the filter loop `O(num_rows)` and pass them to the condition function using `zip()`. This reduced parsing time from 29s to 2.5s for 20k rows.
