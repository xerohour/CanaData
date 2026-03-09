## 2026-03-09 - Pandas Apply Overhead in Nested Data Processing
**Learning:** Using `pandas.Series.apply` with a lambda for element-wise string formatting (like `json.dumps`) has significant overhead. Similarly, looping to prepare a list of dictionaries with a new key is slower than list comprehension with dictionary unpacking.
**Action:** Replace `df[col].apply()` with pure Python list comprehensions over the column's values, and use fast list comprehensions `[dict(item, _key=val) ...]` before `pd.json_normalize()`.
