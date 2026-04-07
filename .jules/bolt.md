
## 2026-04-07 - Dictionary Comprehensions in Large Loops
**Learning:** When repeatedly creating dictionaries with identical keys inside large loops, re-evaluating the dictionary comprehension on every iteration creates a significant CPU bottleneck.
**Action:** Pre-create a base dictionary (`base_dict = {key: 'None' for key in keys}`) outside the loop and use `.copy()` inside the loop.
