## 2024-07-07 - Rate limiter global lock contention
**Learning:** Holding a threading lock during `time.sleep()` for rate limiting causes severe thread contention and blocks all other workers from calculating their wait times.
**Action:** Move the sleep logic outside of the lock context manager by pre-calculating the target sleep times, allowing threads to sleep concurrently.
