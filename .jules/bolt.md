## 2024-04-15 - Identify Horizontal Scaling Bottlenecks
**Learning:** Monolithic in-memory data structures like `self.allMenuItems` guarded by `self._menu_data_lock` ensure data integrity vertically across threads, but the current configuration fundamentally prevents native horizontal scaling across multiple servers.
**Action:** Always flag stateful `threading.Lock()` usage and single-process object dictionaries during architectural reviews when horizontal scalability is the target.
