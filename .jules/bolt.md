## 2024-05-23 - Optimize Repeated Dictionary Creation in Loops
**Learning:** When repeatedly creating dictionaries with identical keys inside large loops, re-evaluating a dictionary comprehension on every iteration creates significant performance overhead due to redundant memory allocation and expression evaluation.
**Action:** Pre-create a base dictionary (`base_dict = {key: 'None' for key in keys}`) outside the loop and use `.copy()` inside the loop, which is significantly faster.
