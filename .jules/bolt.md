## 2024-04-16 - Dictionary Normalization Speedup
**Learning:** When creating a large list of uniform dictionaries from non-uniform data, pre-initializing a template dictionary using `dict.fromkeys(all_keys, 'None')` outside the loop and calling `.copy()` then `.update(item)` inside the loop is nearly 10x faster than using a dictionary comprehension to initialize each item.
**Action:** Always pre-allocate dictionary structures via `dict.fromkeys` and `.copy()` when standardizing keys across massive lists.
