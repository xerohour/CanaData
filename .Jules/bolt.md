## 2024-05-06 - Removed thread locks
**Learning:** Global mutable arrays protected by thread locking forces synchronous write operations which introduces "noisy neighbor" vulnerabilities.
**Action:** Move from global state arrays to stateless worker nodes that aggregate results sequentially in the main thread.
