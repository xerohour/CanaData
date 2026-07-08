## 2026-06-28 - Bottleneck in CanaData global locking
**Learning:** The use of a global `_menu_data_lock` in `process_menu_json` severely degrades performance in multithreaded environments by forcing synchronous write operations to `allMenuItems`.
**Action:** Refactor stateful components into message queues (e.g., Redis Pub/Sub, RabbitMQ) for distributed workers instead of relying on a centralized mutable dictionary to achieve horizontal scaling.
