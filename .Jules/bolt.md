## 2026-10-24 - Scalability and Global Lock Contention Audit
**Learning:** Evaluated real processing logic via stress tests without artificial delays, revealing that \`CanaData._menu_data_lock\` inherently blocks concurrent execution paths.
**Action:** Always replace mock delays (\`time.sleep()\`) with genuine, heavy data payloads when auditing performance under load.
