## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-20 - Fast Pandas JSON Flattening
**Learning:** Re-assigning Pandas string/JSON object representations natively mapped across columns using pure list comprehensions (e.g. `df[col] = [json.dumps(x) for x in df[col]]`) resolves object iterations roughly 5-10% faster than `df[col].apply(lambda x: json.dumps(x))`. Checking `df[col].dtype == 'object'` and `df[col].first_valid_index()` is computationally O(1) compared to `df[col].dropna().head(1)`.
**Action:** Always prefer vectorized Python list comprehension execution inside Pandas dataframes strictly bounded by exact type checks over functional mapping.

## 2024-06-20 - Recursive Dict Optimization
**Learning:** For deep multi-level nested recursion in hot execution paths parsing massive dict structures natively (e.g. `stack`-based while loops), bypassing Python's Method Resolution Order check using explicit type mappings like `type(x) is dict` executes notably faster than `isinstance(x, dict)`. Similarly, caching bound function methods (`keys.pop`, `keys.append`) to the outer scope eliminates costly dict lookups over repeated traversals.
**Action:** Apply bound-method variable caching on stack-implemented while loops handling deep data tree expansions to reduce cumulative execution overhead.
