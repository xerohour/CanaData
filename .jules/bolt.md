## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-24 - Pre-binding vs String Concatenation and Isinstance overhead
**Learning:** The DataFrame batch processor initialization loop relies heavily on the `_flatten_dictionary_custom` method which was using `key = '.'.join(keys + [k])` and multiple `isinstance` checks. This caused string allocation overhead and slow subclass-checking overhead inside a deeply nested recursive loop. In this codebase's architecture where data is strictly derived from `json.load`, objects are guaranteed to be basic primitives.
**Action:** When optimizing tight JSON manipulation loops, cache built-in functions outside the loop (like `join_keys = '.'.join` and `dumps = json.dumps`) and avoid `isinstance` for guaranteed types (use `type(v) is dict`). Append to lists and pop instead of creating new lists via `keys + [k]`.
