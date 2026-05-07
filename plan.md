1. **Refactor `process_menu_json`:**
   - Update `process_menu_json` in `CanaData.py` using `replace_with_git_merge_diff`. Modify lines 544-558 to remove `with self._menu_data_lock:` and return `(listing_id, local_menu_items, emptyMenus_dict, extractedStrains_dict, menu_items_count, totalLocations_list)` instead of directly mutating the global state variables. Note: `emptyMenus_dict` is either empty or has the listing, same for `extractedStrains_dict` and `totalLocations_list`.

2. **Refactor `process_menu_items_json`:**
   - Update `process_menu_items_json` in `CanaData.py` using `replace_with_git_merge_diff`. Modify lines 609-620 to remove `with self._menu_data_lock:` and return the same structure: `(listing_id, local_menu_items, emptyMenus_dict, extractedStrains_dict, menu_items_count, totalLocations_list)` instead of mutating the global state.

3. **Refactor `_fetch_and_process_menu`:**
   - Update `_fetch_and_process_menu` in `CanaData.py` using `replace_with_git_merge_diff`. Modify lines 373-391 to return the processed data returned by `process_menu_json` and `process_menu_items_json` back to the caller instead of returning a boolean. Update exception blocks to return `None`.

4. **Update `_getMenusConcurrent`:**
   - Modify `_getMenusConcurrent` in `CanaData.py` using `replace_with_git_merge_diff`. Update lines 347-354 to aggregate the returned results from `processor.process_locations()`. In the main thread, iterate through `processor.results.values()` and append to `self.allMenuItems`, `self.emptyMenus`, `self.extractedStrains`, `self.menuItemsFound`, and `self.totalLocations`.

5. **Update `_getMenusSequential`:**
   - Modify `_getMenusSequential` in `CanaData.py` using `replace_with_git_merge_diff`. Update lines 328-331 to perform the same state updates sequentially using the newly returned values from `_fetch_and_process_menu`.

6. **Remove legacy `_menu_data_lock` initialization:**
   - Update `__init__` in `CanaData.py` using `replace_with_git_merge_diff` to remove `self._menu_data_lock = threading.Lock()` around line 121.

7. **Refactor `performance_tests/test_stress_concurrency.py`:**
   - Modify `performance_tests/test_stress_concurrency.py` using `replace_with_git_merge_diff` to replace the lock-based logic with a test that instantiates `ConcurrentMenuProcessor(rate_limit=0.0)` and asserts that it correctly aggregates concurrent results without relying on `_menu_data_lock`.

8. **Testing and Verification:**
   - Run the install dependencies command (`/home/jules/.local/share/pipx/venvs/pytest/bin/python -m pip install -r requirements.txt responses pytest-benchmark pandas yattag python-dotenv`) to ensure dependencies are installed in the `pipx` pytest environment.
   - Run the full test suite (`PYTHONPATH=.:./parse-script /home/jules/.local/share/pipx/venvs/pytest/bin/python -m pytest tests/ performance_tests/`) to ensure the `test_stress_concurrency.py` and other benchmarks pass without the "noisy neighbor" issue.

9. **Draft Bolt PR description:**
   - Draft the PR description using the exact required format.
     ```
     ⚡ Bolt: [performance improvement] Remove global thread lock for batched ingestion

     💡 What: Removed `_menu_data_lock` and refactored the worker functions to be stateless. Aggregation is now done in the main thread.
     🎯 Why: The central lock was causing thread contention ("noisy neighbor") under horizontal scaling and high concurrency, throttling performance.
     📊 Impact: Eliminates blocking overhead during the scraping phase, allowing fully unbounded concurrent processing across workers.
     🔬 Measurement: Verified with `performance_tests/test_stress_concurrency.py` that no data is lost and threads do not wait on state mutation.
     ```

10. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
