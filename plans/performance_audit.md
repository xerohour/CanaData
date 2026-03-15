# Performance Audit Plan for CanaData

1. **Create Benchmark Scripts**
   - Use `write_file` to create `scripts/benchmark_concurrency.py` to benchmark the `ConcurrentMenuProcessor`'s `process_locations` method with mocked network calls (using `time.sleep` to simulate latency and disabling rate limits by setting `os.environ['RATE_LIMIT'] = '0'`).
   - Use `write_file` to create `scripts/benchmark_data_processing.py` to compare `OptimizedDataProcessor._flatten_all_items` (using pandas) against the fallback custom flattening method `_flatten_dictionary_custom`, measuring execution time and memory usage.

2. **Verify Benchmark Scripts Creation**
   - Use `list_files` on `scripts/` and `read_file` on both `scripts/benchmark_concurrency.py` and `scripts/benchmark_data_processing.py` to verify their creation and contents.

3. **Run Benchmarks & Profiling**
   - Use `run_in_bash_session` to execute `python3 scripts/benchmark_concurrency.py`.
   - Use `run_in_bash_session` to execute `python3 scripts/benchmark_data_processing.py`.
   - Use `run_in_bash_session` to run `python3 -m cProfile -s cumtime CanaData.py -go all` (or a smaller subset) with a mocked environment or limited scope to gather CPU profiling data and write it to `output/profile_results.txt`.

4. **Create Performance Tests (`tests/test_performance.py`)**
   - Use `write_file` to create `tests/test_performance.py`. This test suite must include tests for:
      - `test_concurrency_latency`: Ensures simulated high-concurrency fetching processes within an expected timeframe (with mocked `requests.get`).
      - `test_thread_safety`: Tests concurrent updates to the shared `_menu_data_lock` in `CanaData` for race conditions.
      - `test_retry_backoff`: Tests `retry_with_backoff` in `concurrent_processor.py`.
      - `test_data_processing_memory`: Checks memory consumption during `organize_into_clean_list`.

5. **Verify Performance Tests Creation**
   - Use `read_file` on `tests/test_performance.py` to verify the test suite code.

6. **Run Performance Tests**
   - Use `run_in_bash_session` to run `python3 -m pytest tests/test_performance.py`.

7. **Generate Performance Audit Report & Update Learnings**
   - Use `write_file` to create `PERFORMANCE_AUDIT_REPORT.md` documenting the findings, identified bottlenecks (e.g., locking in `CanaData`, pandas overhead vs native dict comprehension), and "Before vs. After" optimization projections based on the benchmark results.
   - Use `run_in_bash_session` to create `.jules/bolt.md` documenting critical performance learnings and optimization patterns as per the required format.

8. **Verify Report Creation**
   - Use `read_file` on `PERFORMANCE_AUDIT_REPORT.md` and `.jules/bolt.md` to verify the reports.

9. **Run Full Test Suite and Linters**
   - Use `run_in_bash_session` to run `python3 -m pytest` and `ruff check .` to verify all tests pass and there are no linting regressions.

10. **Pre-Commit Steps**
    - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

11. **Submit Changes**
    - Use `submit` to push the new tests, benchmark scripts, and audit reports with a descriptive branch name and commit message.
