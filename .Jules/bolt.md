## 2024-05-09 - Architecture Transition to Stateless Workers
**Learning:** Using thread locking (`_menu_data_lock`) to synchronize access to a global state variable (`allMenuItems`) creates a significant bottleneck ('noisy neighbor' effect) under high horizontal load.
**Action:** Transitioned architectures to use stateless worker threads that return their processed data independently, followed by sequential aggregation on the main thread, eliminating race conditions and lock contention.
