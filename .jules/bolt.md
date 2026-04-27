## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-15 - Redundant List Copying During Mutation
**Learning:** When a filtering condition (e.g., `if is_match(row)`) in a list comprehension mutates the source element, performing a shallow copy (`row[:]`) in the output expression does not protect the original data. It simply creates redundant copies of already-mutated objects, adding massive CPU and memory overhead.
**Action:** Ensure that data copying for immutability happens *before* mutation logic is executed, or eliminate the redundant copies entirely if the mutation is acceptable.

## 2024-05-15 - Array Mutation in Filter Conditions
**Learning:** Mutating an array (e.g., `row.append(...)`) inside a filtering method like `is_match()` causes side effects on the source data (`self.raw_data`), rendering defensive copying in the list comprehension ineffective and slow.
**Action:** Avoid mutating source arrays during filtering. Instead, compute and store derived values separately, or evaluate them lazily in the rendering step if enrichment isn't strictly necessary for intermediate data structures.
