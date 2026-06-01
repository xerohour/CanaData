1. Fix test failure in `test_stress_locking`
   - `scraper.allMenuItems` in `test_stress_locking` is being overridden to an empty list `[]` instead of dict `{}`.
2. Fix test failure in `tests/test_api.py::test_extract_strains_from_menu`, `tests/test_canadata.py::test_process_menu_json_thread_safe_counts_and_collections` and `test_process_menu_json_thread_safe_deduplicates_extracted_strains`
   - `flush_queue` is not being called by these tests. We need to explicitly call `cana.flush_queue()` inside these tests because we made the update asynchronous in `process_menu_json`.
3. Verify fixes and run tests again.
