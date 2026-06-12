## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-18 - Dictionary Flattening Method Micro-Optimizations
**Learning:** The `flatten_dictionary` method in `CanaData.py` is called hundreds of thousands of times across nested JSON structures. We found that caching method resolution in the inner-most loop for `.append()`, `.pop()` and `'.'.join()`, avoiding `.keys()` overhead on dictionaries using implicit boolean checks (`not v`), and replacing `isinstance` with exact `type` checks on common python types significantly improved CPU-bound dictionary serialization efficiency (~18% faster per loop).
**Action:** When a method processes massive nested recursive structures in tight loops, explicitly cache built-in python methods dynamically, use `not obj` over `len(obj) == 0` for sequences, and order type checking by data likelihood (dictionaries first).
