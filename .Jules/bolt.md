## 2026-05-08 - Stateless Worker Pattern for Concurrent Scraping
**Learning:** Global thread locks (like `_menu_data_lock` around `allMenuItems`) create severe "noisy neighbor" bottlenecks under horizontal scaling, limiting throughput.
**Action:** Use stateless worker nodes that process data locally and return the results for synchronous aggregation on the main thread, rather than locking shared mutable state.
