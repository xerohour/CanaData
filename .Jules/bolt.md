## 2026-06-28 - Removed Centralized Menu Data Lock
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Returning data dictionaries (asynchronous chunk aggregation) from worker methods completely removes the need for centralized thread locking (`_menu_data_lock`), avoiding race conditions and enabling infinite horizontal scaling without thread contention.
