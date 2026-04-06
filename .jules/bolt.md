## 2024-04-06 - Dictionary Comprehension in Loops
**Learning:** When repeatedly creating dictionaries with identical keys inside large loops, re-evaluating a dictionary comprehension on every iteration creates severe performance bottlenecks.
**Action:** Pre-create a base dictionary (`base_dict = {key: 'None' for key in keys}`) outside the loop and use `.copy()` inside the loop, which is significantly faster.
