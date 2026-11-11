## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-08-25 - [Optimize dictionary merges in parsing loop]
**Learning:** When appending or merging data into dictionaries within Python loops (such as during flattening), prefer direct loop key assignments (e.g., `for k, v in data.items(): result[k] = v`) over dictionary comprehensions passed to `.update()`. This avoids the overhead of allocating redundant intermediate dictionary objects.
**Action:** Replaced `.update({...})` calls that dynamically build dictionaries during large loop processing with direct key assignments to save memory and processing time.

## 2024-04-17 - Connection Pooling via requests.Session
**Learning:** The application was making numerous sequential API calls using `requests.get()`, which opens a new TCP connection and performs SSL handshake for every single request. In high-volume scraping, this overhead becomes a significant bottleneck.
**Action:** Use `requests.Session()` to enable connection pooling. This reuses the underlying TCP connections, significantly reducing overhead for repeated API calls to the same host.

## 2026-11-02 - Remove Global Lock Contention in Menu Item Processing
**Learning:** Using a global threading lock (`_menu_data_lock`) to append items to a shared list when running highly concurrent requests (like ThreadPoolExecutor in `CanaData.py`) completely eliminates the benefits of multiprocessing, forcing the application into sequential behavior at the collection step.
**Action:** When gathering high-volume network responses concurrently, local processing functions should return their data back to the dispatcher instead of mutating shared state. The dispatcher can then accumulate or batch the returned values (e.g., using `concurrent.futures.as_completed`) without contention, drastically reducing execution latency.

## 2026-11-20 - Pre-compute string checks and optimize dictionary initialization in loops
**Learning:** Checking string conditions inside loops that iterate over thousands of objects repeatedly creates massive overhead. Furthermore, copying every key-value default iteratively in loops to fill a dict before actual dictionary key matching can cause O(N) operations per item.
**Action:** When evaluating strings in a large batch of items inside loops, pre-compute combinations of specific key attributes using set unions outside the loop. Use `dict.fromkeys(keys, default_value)` instead of loops for populating defaults before adding values from matching specific items.

## 2024-05-18 - O(1) Cache Eviction Optimization
**Learning:** In `CacheManager`, the LRU eviction method `_prune_memory_cache` used `min()` on the dictionary keys with a lambda checking timestamps, making it an O(N) operation. When the cache hits its size limit (e.g., 1000 items), every subsequent insert triggers an O(N) scan.
**Action:** Since Python 3.7+ dictionaries maintain insertion order, implement an O(1) LRU eviction by popping the first item using `next(iter(dict))`. We must ensure accessed items are moved to the end by removing and re-inserting them on hits.
## 2026-11-08 - Pre-compute lowercase string lists in FlowerFilter
**Learning:** Checking string conditions inside list comprehensions that iterate over hundreds of thousands of objects repeatedly creates massive overhead by repeatedly calling `.lower()`.
**Action:** When filtering rows based on categories, brands, stores, strains, and keywords, pre-compute the lowercase string evaluations during `FlowerFilter` load time rather than during inner-loop evaluation in `is_match`. By converting array parameters to lowercase once, execution latency drops from ~0.4s to ~0.05s.

## 2024-05-18 - Dictionary Initialization Iteration
**Learning:** In OptimizedDataProcessor, iterating over `sorted_keys` and checking `if k not in item` is surprisingly much slower than simply iterating over `item.items()` when building a default-initialized dictionary, because most keys in `sorted_keys` are not present in a given item, causing unnecessary string matching and O(1) miss lookups in a tight loop.
**Action:** Replace `for k in sorted_keys: if k not in item: continue; v = item[k]` with `for k, v in item.items():` for faster dictionary population, followed by checking coercions.

## 2026-11-10 - Optimize dictionary initialization inside processing loop
**Learning:** Using `dict.fromkeys(keys, default)` inside a tight processing loop requires CPython to repeatedly iterate over the iterable, hash each element, and insert them one by one. Conversely, `dict.copy()` is highly optimized to clone the underlying hash table's memory directly.
**Action:** When initializing default dictionaries inside a tight loop with identical keys, pre-compute a template dictionary using `dict.fromkeys(keys, default)` outside the loop and use `template.copy()` inside the loop for a significant performance gain.
