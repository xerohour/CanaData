## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-04-26 - Dictionary Organization Performance
**Learning:** Using iterative copying (`.copy()` and `.update()`) in loops for creating uniform dictionaries is significantly slower than dictionary unpacking (`{**template, **item}`) inside list comprehensions.
**Action:** Use list comprehensions with dictionary unpacking for large-scale dictionary generation.

## 2024-04-26 - Avoid Replacing isinstance with Exact Type Checks
**Learning:** Replacing `isinstance(v, list)` with `type(v) is type([])` (or `type() is list`) is a bad practice. It violates duck-typing by failing to match subclasses (like `collections.OrderedDict`), sacrifices readability, and provides no measurable performance gain since `isinstance` is a highly optimized C-level built-in.
**Action:** Never sacrifice code readability and duck-typing for micro-optimizations like exact type checking over `isinstance`.
