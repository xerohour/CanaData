1. **Refactor `process_menu_json` and `process_menu_items_json` to return parsed data instead of mutating state**:
   - `process_menu_json` should return a dict containing: `{'listing_id': listing_id, 'menu_items': local_menu_items, 'empty_menu': empty_menu_dict (or None), 'extracted_strains': local_extracted_strains, 'menu_items_count': menu_items_count, 'listing_copy': listing_copy}`
   - `process_menu_items_json` should do the same.

2. **Refactor `_fetch_and_process_menu` to return the dict from `process_menu_json` or `process_menu_items_json`**. If it fails, it can return `None`.

3. **Update `_getMenusSequential` to process the results**:
   - Iterate over the results of `_fetch_and_process_menu` and apply them to the state.

4. **Update `_getMenusConcurrent` to process the results**:
   - After `processor.process_locations(...)` finishes, we iterate over `processor.results.values()`.
   - Apply the results to the state (`self.allMenuItems`, `self.emptyMenus`, `self.extractedStrains`, `self.menuItemsFound`, and `self.totalLocations`).
   - This eliminates the need for `self._menu_data_lock`.

5. **Remove `self._menu_data_lock` completely**:
   - Remove it from `__init__`.

6. **Fix the benchmarking tests**:
   - Update `performance_tests/test_stress_concurrency.py` because `self.allMenuItems` won't be protected by a lock anymore. Since the test explicitly tests the locking bottleneck, we should rewrite it to test `ConcurrentMenuProcessor` without locks. Wait, if the test is "test_stress_concurrency.py" and we remove the lock, we should test the new mechanism of gathering results using `ConcurrentMenuProcessor` and then updating state.

7. **Add to `.Jules/bolt.md` (Performance Learning)**:
   - "## YYYY-MM-DD - Fix Thread Lock Contention"
   - Learning: Global mutable arrays protected by thread locks create synchronous bottlenecks ("noisy neighbor" problem) during horizontal scaling and high concurrency, preventing true parallel throughput.
   - Action: Shift to stateless worker nodes where worker threads return results individually, and the main thread aggregates them without locks, ensuring safe and unblocked execution.

8. **Pre-commit steps**:
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

9. **Submit**: Create PR.
