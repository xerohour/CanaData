## 2026-07-03 - Replace Pandas with Pure Python for JSON Flattening
**Learning:** When flattening and normalizing large, predictable JSON API payloads into dictionaries, pandas.json_normalize() introduces massive overhead due to type inference and DataFrame instantiation. Pure Python list comprehensions and dictionary unpacking ({**template, **item}) perform significantly better.
**Action:** Always prefer pure Python list comprehensions and dict unpacking over Pandas for flattening predictable JSON structures to reduce latency and memory overhead.
## 2026-07-03 - Code Review Fixes for Pure Python Translation
**Learning:** Translating a Pandas optimization to Pure Python requires ensuring internal helper functions (like `_normalize_data`) also transition away from Pandas data types (DataFrames) to pure Python lists/dicts to prevent logic regressions. Furthermore, watch out for naive initialization parameters like the string `"None"` which can break downstream null checks.
**Action:** Always maintain full integration logic when swapping library internals.
