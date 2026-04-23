import logging
import os
import queue
import subprocess
import sys
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import tkinter as tk
from tkinter import messagebox, ttk


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from CanaData import CanaData  # noqa: E402  # noqa: E402


@dataclass
class RunConfig:
    source: str
    slug_mode: str
    slug_value: str
    include_storefronts: bool
    include_deliveries: bool
    fetch_brands: bool
    fetch_strains: bool
    test_mode: bool
    concurrent: bool
    max_workers: int
    rate_limit: float
    page_size: int
    cache_enabled: bool
    optimize_processing: bool


class QueueLogHandler(logging.Handler):
    def __init__(self, event_queue: queue.Queue):
        super().__init__()
        self.event_queue = event_queue

    def emit(self, record: logging.LogRecord) -> None:
        self.event_queue.put(("log", self.format(record), record.levelname))


class CanaDataGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CanaData Desktop")
        self.root.geometry("1100x760")
        self.root.minsize(960, 680)

        self.event_queue: queue.Queue = queue.Queue()
        self.run_thread: threading.Thread | None = None
        self.cancel_requested = threading.Event()
        self.running = False
        self.last_output_dir = self._default_output_dir()

        self._build_variables()
        self._build_ui()
        self._bind_events()
        self._update_slug_mode_ui()
        self.root.after(120, self._poll_events)

    def _build_variables(self) -> None:
        self.source_var = tk.StringVar(value="weedmaps")
        self.slug_mode_var = tk.StringVar(value="single")
        self.slug_value_var = tk.StringVar(value="colorado")

        self.storefronts_var = tk.BooleanVar(value=True)
        self.deliveries_var = tk.BooleanVar(value=True)
        self.fetch_brands_var = tk.BooleanVar(value=False)
        self.fetch_strains_var = tk.BooleanVar(value=False)
        self.test_mode_var = tk.BooleanVar(value=False)

        self.concurrent_var = tk.BooleanVar(value=True)
        self.max_workers_var = tk.StringVar(value="10")
        self.rate_limit_var = tk.StringVar(value="1.0")
        self.page_size_var = tk.StringVar(value="100")
        self.cache_var = tk.BooleanVar(value=True)
        self.optimize_var = tk.BooleanVar(value=True)

        self.progress_text_var = tk.StringVar(value="Ready")
        self.summary_var = tk.StringVar(value="No runs yet")

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(container)
        top.pack(fill=tk.X)

        self._build_run_source_section(top)
        self._build_scope_section(top)
        self._build_data_section(top)
        self._build_perf_section(top)

        controls = ttk.Frame(container, padding=(0, 10, 0, 8))
        controls.pack(fill=tk.X)
        self.start_button = ttk.Button(controls, text="Start Run", command=self.start_run)
        self.start_button.pack(side=tk.LEFT)
        self.cancel_button = ttk.Button(controls, text="Cancel", command=self.cancel_run, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=8)
        ttk.Button(controls, text="Open Output Folder", command=self.open_output_folder).pack(side=tk.LEFT)

        self.progressbar = ttk.Progressbar(container, mode="determinate", maximum=100)
        self.progressbar.pack(fill=tk.X)
        ttk.Label(container, textvariable=self.progress_text_var).pack(anchor=tk.W, pady=(4, 8))

        logs_frame = ttk.LabelFrame(container, text="Live Log")
        logs_frame.pack(fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(logs_frame, wrap=tk.WORD, height=18)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(logs_frame, command=self.log_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scroll.set)
        self.log_text.configure(state=tk.DISABLED)

        summary_frame = ttk.Frame(container, padding=(0, 8, 0, 0))
        summary_frame.pack(fill=tk.X)
        ttk.Label(summary_frame, text="Summary:").pack(side=tk.LEFT)
        ttk.Label(summary_frame, textvariable=self.summary_var).pack(side=tk.LEFT, padx=8)

    def _build_run_source_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Source", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        for text, value in (("Weedmaps", "weedmaps"), ("Leafly", "leafly"), ("CannMenus", "cannmenus")):
            ttk.Radiobutton(section, text=text, variable=self.source_var, value=value).pack(anchor=tk.W)

    def _build_scope_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Scope", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        for text, value in (
            ("Single Slug", "single"),
            ("All States (states.txt)", "all"),
            ("My List (mylist.txt)", "mylist"),
            ("Known Slugs (slugs.txt)", "slugs"),
        ):
            ttk.Radiobutton(section, text=text, variable=self.slug_mode_var, value=value).pack(anchor=tk.W)

        row = ttk.Frame(section)
        row.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(row, text="Slug:").pack(side=tk.LEFT)
        self.slug_entry = ttk.Entry(row, textvariable=self.slug_value_var)
        self.slug_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

    def _build_data_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Data Options", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        ttk.Checkbutton(section, text="Storefronts", variable=self.storefronts_var).pack(anchor=tk.W)
        ttk.Checkbutton(section, text="Deliveries", variable=self.deliveries_var).pack(anchor=tk.W)
        ttk.Checkbutton(section, text="Fetch Brands", variable=self.fetch_brands_var).pack(anchor=tk.W)
        ttk.Checkbutton(section, text="Fetch Strains", variable=self.fetch_strains_var).pack(anchor=tk.W)
        ttk.Checkbutton(section, text="Troubleshooting Logs", variable=self.test_mode_var).pack(anchor=tk.W)

    def _build_perf_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Performance", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Checkbutton(section, text="Concurrent Menus", variable=self.concurrent_var).pack(anchor=tk.W)
        ttk.Checkbutton(section, text="Enable Cache", variable=self.cache_var).pack(anchor=tk.W)
        ttk.Checkbutton(section, text="Optimized Processing", variable=self.optimize_var).pack(anchor=tk.W)

        self._labeled_entry(section, "Max workers", self.max_workers_var)
        self._labeled_entry(section, "Rate limit (sec)", self.rate_limit_var)
        self._labeled_entry(section, "Page size", self.page_size_var)

    def _labeled_entry(self, parent: ttk.Frame, label: str, var: tk.StringVar) -> None:
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=(4, 0))
        ttk.Label(row, text=label, width=14).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=var, width=10).pack(side=tk.LEFT)

    def _bind_events(self) -> None:
        self.slug_mode_var.trace_add("write", lambda *_: self._update_slug_mode_ui())

    def _update_slug_mode_ui(self) -> None:
        mode = self.slug_mode_var.get()
        state = tk.NORMAL if mode == "single" else tk.DISABLED
        self.slug_entry.configure(state=state)

    def _validate_config(self) -> RunConfig | None:
        slug_mode = self.slug_mode_var.get()
        slug_value = self.slug_value_var.get().strip().lower()
        if slug_mode == "single" and not slug_value:
            messagebox.showerror("Missing Slug", "Enter a city/state slug for single mode.")
            return None

        if not self.storefronts_var.get() and not self.deliveries_var.get() and self.source_var.get() == "weedmaps":
            messagebox.showerror("No Retailer Type", "Select at least one of Storefronts or Deliveries.")
            return None

        try:
            max_workers = int(self.max_workers_var.get())
            page_size = int(self.page_size_var.get())
            rate_limit = float(self.rate_limit_var.get())
            if max_workers < 1 or page_size < 1 or rate_limit < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Numbers", "Max workers/page size must be >= 1 and rate limit >= 0.")
            return None

        return RunConfig(
            source=self.source_var.get(),
            slug_mode=slug_mode,
            slug_value=slug_value,
            include_storefronts=self.storefronts_var.get(),
            include_deliveries=self.deliveries_var.get(),
            fetch_brands=self.fetch_brands_var.get(),
            fetch_strains=self.fetch_strains_var.get(),
            test_mode=self.test_mode_var.get(),
            concurrent=self.concurrent_var.get(),
            max_workers=max_workers,
            rate_limit=rate_limit,
            page_size=page_size,
            cache_enabled=self.cache_var.get(),
            optimize_processing=self.optimize_var.get(),
        )

    def start_run(self) -> None:
        if self.running:
            return

        config = self._validate_config()
        if not config:
            return

        self.running = True
        self.cancel_requested.clear()
        self.start_button.configure(state=tk.DISABLED)
        self.cancel_button.configure(state=tk.NORMAL)
        self.progressbar.configure(value=0)
        self.progress_text_var.set("Starting...")
        self.summary_var.set("Run in progress")
        self._append_log("Run started", "INFO")

        self.run_thread = threading.Thread(target=self._run_pipeline, args=(config,), daemon=True)
        self.run_thread.start()

    def cancel_run(self) -> None:
        if not self.running:
            return
        self.cancel_requested.set()
        self.progress_text_var.set("Cancellation requested. Waiting for current step to finish...")
        self._append_log("Cancellation requested", "WARNING")

    def _run_pipeline(self, config: RunConfig) -> None:
        logger_name = "CanaData"
        handler = QueueLogHandler(self.event_queue)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)

        try:
            self._set_runtime_env(config)
            cana = CanaData(
                max_workers=config.max_workers,
                rate_limit=config.rate_limit,
                cache_enabled=config.cache_enabled,
                optimize_processing=config.optimize_processing,
                interactive_mode=False,
            )
            cana.storefronts = config.include_storefronts
            cana.deliveries = config.include_deliveries
            if config.test_mode:
                cana.test_mode()

            slugs = self._resolve_slugs(config)
            if config.slug_mode == "single":
                run_label = config.slug_value
            else:
                run_label = f"{config.slug_mode} ({len(slugs)} slugs)"
            self.event_queue.put(("progress_text", f"Preparing run for {run_label}"))

            if config.fetch_brands:
                self.event_queue.put(("progress_text", "Fetching global brands"))
                cana.get_brands()

            if config.fetch_strains:
                self.event_queue.put(("progress_text", "Fetching global strains"))
                cana.get_strains()

            metadata_only = (
                config.source == "weedmaps"
                and (config.fetch_brands or config.fetch_strains)
                and config.slug_mode == "single"
                and config.slug_value in {"", "global"}
            )

            run_summaries: List[str] = []

            if metadata_only:
                cana.set_city_slug("global")
                cana.data_to_csv()
                run_summaries.append("metadata exported")
            else:
                total = max(1, len(slugs))
                for index, slug in enumerate(slugs, start=1):
                    if self.cancel_requested.is_set():
                        self.event_queue.put(("progress_text", "Cancelled"))
                        self.event_queue.put(("cancelled", "Run cancelled by user"))
                        return

                    self.event_queue.put(("progress", int(((index - 1) / total) * 100)))
                    self.event_queue.put(("progress_text", f"[{index}/{total}] Processing {slug}"))

                    cana.set_city_slug(slug)
                    if config.source == "leafly":
                        cana.get_leafly_data()
                    elif config.source == "cannmenus":
                        cana.get_cannmenus_data()
                    else:
                        cana.get_locations()
                        if not cana.NonGreenState:
                            cana.get_menus()

                    cana.data_to_csv()
                    run_summaries.append(
                        f"{slug}: {cana.locationsFound} locations, {cana.menuItemsFound} items"
                    )
                    cana.reset_data_sets()

                self.event_queue.put(("progress", 100))

            self.last_output_dir = self._default_output_dir()
            summary = " | ".join(run_summaries[:3])
            if len(run_summaries) > 3:
                summary += f" | +{len(run_summaries) - 3} more"
            if not summary:
                summary = "Completed"

            self.event_queue.put(("done", summary))
        except Exception as exc:
            self.event_queue.put(("error", str(exc)))
        finally:
            logger.removeHandler(handler)

    def _set_runtime_env(self, config: RunConfig) -> None:
        os.environ["PAGE_SIZE"] = str(config.page_size)
        os.environ["USE_CONCURRENT_PROCESSING"] = "true" if config.concurrent else "false"
        os.environ["MAX_WORKERS"] = str(config.max_workers)
        os.environ["RATE_LIMIT"] = str(config.rate_limit)

    def _resolve_slugs(self, config: RunConfig) -> List[str]:
        if config.slug_mode == "single":
            return [config.slug_value]
        if config.slug_mode == "all":
            return self._read_slug_file(ROOT / "states.txt")
        if config.slug_mode == "mylist":
            return self._read_slug_file(ROOT / "mylist.txt")
        if config.slug_mode == "slugs":
            return self._read_slug_file(ROOT / "slugs.txt")
        return [config.slug_value]

    def _read_slug_file(self, path: Path) -> List[str]:
        if not path.exists():
            raise FileNotFoundError(f"Missing slug file: {path.name}")
        lines = [line.strip().lower().replace(" ", "-") for line in path.read_text(encoding="utf-8").splitlines()]
        slugs = [line for line in lines if line]
        if not slugs:
            raise ValueError(f"No slugs found in {path.name}")
        return slugs

    def _poll_events(self) -> None:
        try:
            while True:
                event = self.event_queue.get_nowait()
                kind = event[0]
                if kind == "log":
                    _, message, level = event
                    self._append_log(message, level)
                elif kind == "progress":
                    self.progressbar.configure(value=event[1])
                elif kind == "progress_text":
                    self.progress_text_var.set(event[1])
                elif kind == "done":
                    self._finish_run(success=True, summary=event[1])
                elif kind == "cancelled":
                    self._finish_run(success=False, summary=event[1])
                elif kind == "error":
                    self._finish_run(success=False, summary=f"Failed: {event[1]}")
                    messagebox.showerror("Run Failed", event[1])
        except queue.Empty:
            pass
        finally:
            self.root.after(120, self._poll_events)

    def _finish_run(self, success: bool, summary: str) -> None:
        self.running = False
        self.start_button.configure(state=tk.NORMAL)
        self.cancel_button.configure(state=tk.DISABLED)
        self.progress_text_var.set("Completed" if success else "Stopped")
        self.summary_var.set(summary)
        level = "INFO" if success else "WARNING"
        self._append_log(summary, level)

    def _append_log(self, text: str, level: str) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{text}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _default_output_dir(self) -> Path:
        folder = f"CanaData_{datetime.now().strftime('%m-%d-%Y')}"
        return ROOT / folder

    def open_output_folder(self) -> None:
        target = self.last_output_dir if self.last_output_dir.exists() else ROOT
        if sys.platform.startswith("win"):
            os.startfile(str(target))  # type: ignore[attr-defined]
            return
        if sys.platform == "darwin":
            subprocess.run(["open", str(target)], check=False)
            return
        subprocess.run(["xdg-open", str(target)], check=False)


def main() -> None:
    root = tk.Tk()
    __app = CanaDataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
