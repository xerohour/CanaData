## 2026-03-17 - Pandas json_normalize vs Pure Python Flattening overhead
**Learning:** Benchmarking in `optimized_data_processor.py` indicates that `pd.json_normalize` coupled with `df[col].apply()` introduces significant overhead (slower by ~40%) for heavily nested, small-scoped dictionary structures compared to a custom iterative python fallback and list comprehensions.
**Action:** Always favor native Python list comprehensions over Pandas Series `.apply(lambda x: ...)` for element-wise string mapping and prefer custom iterative flattening for JSON structures before invoking DataFrame creation.

## 2026-03-17 - Concurrency Performance Testing
**Learning:** When performing parallel concurrency latency profiling on `CanaData`, API rate limits skew real application logic performance execution times.
**Action:** Ensure the environment rate limit is disabled by setting `os.environ['RATE_LIMIT'] = '0'` and mock the network layer (e.g., `@patch('CanaData.CanaData.do_request')`) utilizing `time.sleep()` to isolate network delays.