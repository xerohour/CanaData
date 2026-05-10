## 2024-05-15 - [Stateless Concurrent Workers]
**Learning:** Thread locking on a global mutable state array (`_menu_data_lock` with `allMenuItems`) creates severe "noisy neighbor" bottlenecks under high horizontal load.
**Action:** Always refactor concurrent processing tasks to use stateless worker threads that return results individually, and aggregate these results synchronously on the main thread to prevent lock contention.
