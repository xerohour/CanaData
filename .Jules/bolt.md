## 2024-07-04 - Pure Python Optimization over Pandas
**Learning:** For flattening and normalizing large, predictable JSON API payloads into dictionaries or CSV-ready structures, pure Python list comprehensions and dictionary unpacking outperform `pandas.json_normalize()` by avoiding massive overhead due to type inference, casting, and DataFrame instantiation.
**Action:** Prefer pure Python dictionary unpacking and list comprehensions (e.g. `{**template, **item}`) when normalizing JSON lists into uniform structures, instead of importing pandas.
