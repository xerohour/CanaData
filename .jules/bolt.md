## 2024-05-19 - Pre-computing row strings
**Learning:** In list comprehensions that evaluate multiple conditions (e.g., across multiple filters), repeatedly joining entire rows into strings (`" ".join([str(x) for x in row]).lower()`) inside the evaluation condition causes severe performance bottlenecks (`O(num_filters * num_rows)`).
**Action:** Always pre-compute and cache expensive row transformations (`row_str`) outside the filter loop (`O(num_rows)`) and pass them directly into the evaluation condition to significantly improve performance.
