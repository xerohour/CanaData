## 2026-07-05 - Global Lock Contention in Concurrent Processing
**Learning:** Using a global lock for synchronizing writes to a shared state array completely negates multithreading benefits under high concurrency.
**Action:** Transition to stateless worker nodes and asynchronous message queues for scalable data aggregation.
