## 2024-05-15 - [CanaData] Rate Limiter Bottlenecks
**Learning:** Global rate limiting via a shared lock where threads sleep *inside* the lock (`time.sleep(sleep_time)`) acts as a significant concurrency bottleneck.
**Action:** Calculate the expected future execution time inside the lock and advance the tracker, but release the lock before calling `time.sleep()`. This ensures the rate limit is enforced globally without deadlocking other threads from doing their calculations.
