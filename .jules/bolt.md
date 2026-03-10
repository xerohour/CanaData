## 2025-03-10 - Pandas Series Overhead vs List Comprehensions
**Learning:** Pandas `.apply()` incurs significant overhead for element-wise string formatting or mapping (like `json.dumps` over nested objects) compared to pure Python list comprehensions. The overhead of mapping each item through Pandas series objects makes list comprehensions consistently 5-10% faster for operations where vectorization isn't possible.
**Action:** When handling string conversions, JSON serialization, or other element-wise operations on DataFrame columns that can't be strictly vectorized, bypass Pandas `.apply()` and use pure Python list comprehensions over the column's values (e.g., `df[col] = [json.dumps(x) ... for x in df[col]]`).

## 2025-03-10 - Fast Dictionary Copying in Loops
**Learning:** Using `item_copy = item.copy()` and `append` within nested loops to construct a flat list of items is slower than using a list comprehension with dictionary unpacking (`[dict(item, new_key=val) for ...]`).
**Action:** When flattening data structures or pre-processing lists of dictionaries, prefer list comprehensions with dictionary unpacking to minimize the function call overhead of `.copy()` and `.append()`.
