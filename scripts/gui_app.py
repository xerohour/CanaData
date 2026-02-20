import logging
import os
import queue
import subprocess
import sys
import threading
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import tkinter as tk
from tkinter import messagebox, ttk


ROOT = Path(__file__).resolve().parents[1]
GUI_SETTINGS_PATH = ROOT / ".gui_settings.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from CanaData import CanaData


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
        self.root.option_add("*tearOff", False)

        self.event_queue: queue.Queue = queue.Queue()
        self.run_thread: threading.Thread | None = None
        self.cancel_requested = threading.Event()
        self.running = False
        self.pending_close = False
        self.last_output_dir = self._default_output_dir()
        self.run_started_at: datetime | None = None
        self.config_widgets: List[tk.Widget] = []
        self.total_locations_processed = 0
        self.total_items_processed = 0

        self._build_variables()
        self._load_settings()
        self._build_ui()
        self._bind_events()
        self._update_slug_mode_ui()
        self._update_source_ui()
        self._refresh_run_readiness()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
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
        self.status_var = tk.StringVar(value="Idle")
        self.slug_label_var = tk.StringVar(value="Slug:")
        self.scope_hint_var = tk.StringVar(value="Single mode: run one slug.")
        self.metrics_var = tk.StringVar(value="Runs: 0 | Locations: 0 | Items: 0")
        self.form_error_var = tk.StringVar(value="")
        self.autoscroll_var = tk.BooleanVar(value=True)

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
        self.open_button = ttk.Button(controls, text="Open Output Folder", command=self.open_output_folder)
        self.open_button.pack(side=tk.LEFT)
        self.clear_log_button = ttk.Button(controls, text="Clear Log", command=self._clear_log)
        self.clear_log_button.pack(side=tk.LEFT, padx=(8, 0))
        ttk.Checkbutton(controls, text="Auto-scroll", variable=self.autoscroll_var).pack(side=tk.RIGHT)

        self.progressbar = ttk.Progressbar(container, mode="determinate", maximum=100)
        self.progressbar.pack(fill=tk.X)
        status_row = ttk.Frame(container)
        status_row.pack(fill=tk.X, pady=(4, 8))
        ttk.Label(status_row, text="Status:").pack(side=tk.LEFT)
        ttk.Label(status_row, textvariable=self.status_var).pack(side=tk.LEFT, padx=(4, 12))
        ttk.Label(status_row, textvariable=self.progress_text_var).pack(side=tk.LEFT)
        ttk.Label(status_row, textvariable=self.metrics_var).pack(side=tk.RIGHT)

        form_error_row = ttk.Frame(container)
        form_error_row.pack(fill=tk.X)
        ttk.Label(form_error_row, textvariable=self.form_error_var, foreground="#991b1b").pack(anchor=tk.W)

        logs_frame = ttk.LabelFrame(container, text="Live Log")
        logs_frame.pack(fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(logs_frame, wrap=tk.WORD, height=18)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(logs_frame, command=self.log_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scroll.set)
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.tag_configure("INFO", foreground="#1e3a8a")
        self.log_text.tag_configure("WARNING", foreground="#92400e")
        self.log_text.tag_configure("ERROR", foreground="#991b1b")

        summary_frame = ttk.Frame(container, padding=(0, 8, 0, 0))
        summary_frame.pack(fill=tk.X)
        ttk.Label(summary_frame, text="Summary:").pack(side=tk.LEFT)
        ttk.Label(summary_frame, textvariable=self.summary_var).pack(side=tk.LEFT, padx=8)
        ttk.Label(summary_frame, textvariable=self.scope_hint_var).pack(side=tk.RIGHT)

        hint_row = ttk.Frame(container, padding=(0, 4, 0, 0))
        hint_row.pack(fill=tk.X)
        ttk.Label(
            hint_row,
            text="Shortcuts: Ctrl+Enter start run, Esc cancel run",
        ).pack(side=tk.RIGHT)

        if self.slug_entry not in self.config_widgets:
            self.config_widgets.append(self.slug_entry)

    def _build_run_source_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Source", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        for text, value in (("Weedmaps", "weedmaps"), ("Leafly", "leafly"), ("CannMenus", "cannmenus")):
            rb = ttk.Radiobutton(section, text=text, variable=self.source_var, value=value)
            rb.pack(anchor=tk.W)
            self.config_widgets.append(rb)

    def _build_scope_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Scope", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        for text, value in (
            ("Single Slug", "single"),
            ("All States (states.txt)", "all"),
            ("My List (mylist.txt)", "mylist"),
            ("Known Slugs (slugs.txt)", "slugs"),
        ):
            rb = ttk.Radiobutton(section, text=text, variable=self.slug_mode_var, value=value)
            rb.pack(anchor=tk.W)
            self.config_widgets.append(rb)

        row = ttk.Frame(section)
        row.pack(fill=tk.X, pady=(6, 0))
        ttk.Label(row, textvariable=self.slug_label_var).pack(side=tk.LEFT)
        self.slug_entry = ttk.Entry(row, textvariable=self.slug_value_var)
        self.slug_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

    def _build_data_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Data Options", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        self.storefronts_check = ttk.Checkbutton(section, text="Storefronts", variable=self.storefronts_var)
        self.storefronts_check.pack(anchor=tk.W)
        self.deliveries_check = ttk.Checkbutton(section, text="Deliveries", variable=self.deliveries_var)
        self.deliveries_check.pack(anchor=tk.W)
        self.fetch_brands_check = ttk.Checkbutton(section, text="Fetch Brands", variable=self.fetch_brands_var)
        self.fetch_brands_check.pack(anchor=tk.W)
        self.fetch_strains_check = ttk.Checkbutton(section, text="Fetch Strains", variable=self.fetch_strains_var)
        self.fetch_strains_check.pack(anchor=tk.W)
        self.test_mode_check = ttk.Checkbutton(section, text="Troubleshooting Logs", variable=self.test_mode_var)
        self.test_mode_check.pack(anchor=tk.W)
        self.config_widgets.extend(
            [
                self.storefronts_check,
                self.deliveries_check,
                self.fetch_brands_check,
                self.fetch_strains_check,
                self.test_mode_check,
            ]
        )

    def _build_perf_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="Performance", padding=8)
        section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.concurrent_check = ttk.Checkbutton(section, text="Concurrent Menus", variable=self.concurrent_var)
        self.concurrent_check.pack(anchor=tk.W)
        self.cache_check = ttk.Checkbutton(section, text="Enable Cache", variable=self.cache_var)
        self.cache_check.pack(anchor=tk.W)
        self.optimize_check = ttk.Checkbutton(section, text="Optimized Processing", variable=self.optimize_var)
        self.optimize_check.pack(anchor=tk.W)

        self.max_workers_entry = self._labeled_entry(section, "Max workers", self.max_workers_var)
        self.rate_limit_entry = self._labeled_entry(section, "Rate limit (sec)", self.rate_limit_var)
        self.page_size_entry = self._labeled_entry(section, "Page size", self.page_size_var)
        self.config_widgets.extend(
            [
                self.concurrent_check,
                self.cache_check,
                self.optimize_check,
                self.max_workers_entry,
                self.rate_limit_entry,
                self.page_size_entry,
            ]
        )

    def _labeled_entry(self, parent: ttk.Frame, label: str, var: tk.StringVar) -> ttk.Entry:
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=(4, 0))
        ttk.Label(row, text=label, width=14).pack(side=tk.LEFT)
        entry = ttk.Entry(row, textvariable=var, width=10)
        entry.pack(side=tk.LEFT)
        return entry

    def _bind_events(self) -> None:
        self.slug_mode_var.trace_add("write", lambda *_: self._update_slug_mode_ui())
        self.source_var.trace_add("write", lambda *_: self._update_source_ui())
        self.slug_mode_var.trace_add("write", lambda *_: self._update_scope_hint())
        self.slug_value_var.trace_add("write", lambda *_: self._update_scope_hint())
        self.source_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.slug_mode_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.slug_value_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.storefronts_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.deliveries_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.max_workers_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.rate_limit_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.page_size_var.trace_add("write", lambda *_: self._refresh_run_readiness())
        self.root.bind("<Control-Return>", lambda *_: self.start_run())
        self.root.bind("<Escape>", lambda *_: self.cancel_run())

    def _update_slug_mode_ui(self) -> None:
        mode = self.slug_mode_var.get()
        state = tk.NORMAL if mode == "single" and not self.running else tk.DISABLED
        self.slug_entry.configure(state=state)

    def _update_scope_hint(self) -> None:
        source = self.source_var.get()
        mode = self.slug_mode_var.get()

        if source == "leafly":
            if mode == "single":
                slug = self.slug_value_var.get().strip()
                self.scope_hint_var.set(f"Leafly mode: {slug or '<slug required>'}")
            else:
                self.scope_hint_var.set("Leafly mode: bulk slug files supported")
            return

        if source == "cannmenus":
            if mode == "single":
                slug = self.slug_value_var.get().strip()
                self.scope_hint_var.set(f"CannMenus mode: {slug or '<2-letter state code>'}")
            else:
                file_map = {
                    "all": ROOT / "states.txt",
                    "mylist": ROOT / "mylist.txt",
                    "slugs": ROOT / "slugs.txt",
                }
                source_file = file_map.get(mode)
                if not source_file:
                    self.scope_hint_var.set("CannMenus mode")
                    return
                if not source_file.exists():
                    self.scope_hint_var.set(f"Missing {source_file.name}")
                    return
                rows = [line.strip().lower() for line in source_file.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
                invalid = [slug for slug in rows if len(slug) != 2 or not slug.isalpha()]
                self.scope_hint_var.set(
                    f"{source_file.name}: {len(rows)} entries, {len(invalid)} invalid for CannMenus"
                )
            return

        if mode == "single":
            slug = self.slug_value_var.get().strip()
            self.scope_hint_var.set(f"Single mode: {slug or '<slug required>'}")
            return

        file_map = {
            "all": ROOT / "states.txt",
            "mylist": ROOT / "mylist.txt",
            "slugs": ROOT / "slugs.txt",
        }
        source_file = file_map.get(mode)
        if not source_file:
            self.scope_hint_var.set("")
            return
        if not source_file.exists():
            self.scope_hint_var.set(f"Missing {source_file.name}")
            return
        count = len([line for line in source_file.read_text(encoding="utf-8").splitlines() if line.strip()])
        self.scope_hint_var.set(f"{source_file.name}: {count} slugs")

    def _compute_validation_error(self) -> str | None:
        slug_mode = self.slug_mode_var.get()
        slug_value = self.slug_value_var.get().strip().lower()
        source = self.source_var.get()

        if slug_mode == "single" and not slug_value:
            return "Enter a slug for single mode"

        if source == "cannmenus" and slug_mode == "single":
            if len(slug_value) != 2 or not slug_value.isalpha():
                return "CannMenus single mode requires 2-letter state code (e.g. ca, ny)"

        if source == "weedmaps" and not self.storefronts_var.get() and not self.deliveries_var.get():
            return "Select at least one retailer type (Storefronts or Deliveries)"

        try:
            max_workers = int(self.max_workers_var.get())
            page_size = int(self.page_size_var.get())
            rate_limit = float(self.rate_limit_var.get())
            if max_workers < 1 or page_size < 1 or rate_limit < 0:
                return "Max workers/page size must be >= 1 and rate limit must be >= 0"
        except ValueError:
            return "Max workers/page size must be integers and rate limit a number"

        if slug_mode in {"all", "mylist", "slugs"}:
            file_map = {
                "all": ROOT / "states.txt",
                "mylist": ROOT / "mylist.txt",
                "slugs": ROOT / "slugs.txt",
            }
            slug_file = file_map[slug_mode]
            if not slug_file.exists():
                return f"Missing {slug_file.name}"
            values = [line.strip() for line in slug_file.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
            if not values:
                return f"{slug_file.name} has no usable entries"
            if source == "cannmenus":
                invalid = [slug for slug in values if len(slug) != 2 or not slug.isalpha()]
                if invalid:
                    return f"{slug_file.name} contains non-2-letter entries for CannMenus"

        return None

    def _refresh_run_readiness(self) -> None:
        if self.running:
            return
        error = self._compute_validation_error()
        if error:
            self.start_button.configure(state=tk.DISABLED)
            self.form_error_var.set(error)
            return
        self.start_button.configure(state=tk.NORMAL, text="Start Run")
        self.form_error_var.set("")

    def _update_source_ui(self) -> None:
        source = self.source_var.get()
        is_weedmaps = source == "weedmaps"

        self.slug_label_var.set("State Code:" if source == "cannmenus" else "Slug:")

        widget_state = tk.NORMAL if is_weedmaps and not self.running else tk.DISABLED
        for widget in (
            self.storefronts_check,
            self.deliveries_check,
            self.concurrent_check,
            self.max_workers_entry,
            self.rate_limit_entry,
            self.fetch_brands_check,
            self.fetch_strains_check,
        ):
            widget.configure(state=widget_state)

        if not is_weedmaps:
            self.storefronts_var.set(True)
            self.deliveries_var.set(True)
            self.fetch_brands_var.set(False)
            self.fetch_strains_var.set(False)

        self._update_scope_hint()

    def _validate_config(self) -> RunConfig | None:
        error = self._compute_validation_error()
        if error:
            messagebox.showerror("Invalid Configuration", error)
            return None

        slug_mode = self.slug_mode_var.get()
        slug_value = self.slug_value_var.get().strip().lower()
        max_workers = int(self.max_workers_var.get())
        page_size = int(self.page_size_var.get())
        rate_limit = float(self.rate_limit_var.get())

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
        self.pending_close = False
        self.cancel_requested.clear()
        self._save_settings()
        self.run_started_at = datetime.now()
        self.start_button.configure(state=tk.DISABLED, text="Running...")
        self.cancel_button.configure(state=tk.NORMAL)
        self._set_controls_state(locked=True)
        self.progressbar.configure(value=0)
        self.progress_text_var.set("Starting...")
        self.status_var.set("Running")
        self.summary_var.set("Run in progress")
        self.form_error_var.set("")
        self.metrics_var.set("Runs: 0 | Locations: 0 | Items: 0")
        self.total_locations_processed = 0
        self.total_items_processed = 0
        self._append_log("Run started", "INFO")

        self.run_thread = threading.Thread(target=self._run_pipeline, args=(config,), daemon=True)
        self.run_thread.start()

    def cancel_run(self) -> None:
        if not self.running:
            return
        self.cancel_requested.set()
        self.cancel_button.configure(state=tk.DISABLED)
        self.progress_text_var.set("Cancellation requested. Waiting for current step to finish...")
        self.status_var.set("Cancelling")
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
            slugs_completed = 0

            if metadata_only:
                cana.set_city_slug("global")
                cana.data_to_csv()
                run_summaries.append("metadata exported")
                self.event_queue.put(("metrics", 1, 0, 0))
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
                    slugs_completed += 1
                    self.total_locations_processed += cana.locationsFound
                    self.total_items_processed += cana.menuItemsFound
                    self.event_queue.put(("metrics", slugs_completed, self.total_locations_processed, self.total_items_processed))
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
            slugs = [config.slug_value]
        elif config.slug_mode == "all":
            slugs = self._read_slug_file(ROOT / "states.txt")
        elif config.slug_mode == "mylist":
            slugs = self._read_slug_file(ROOT / "mylist.txt")
        elif config.slug_mode == "slugs":
            slugs = self._read_slug_file(ROOT / "slugs.txt")
        else:
            slugs = [config.slug_value]

        if config.source == "cannmenus":
            invalid = [slug for slug in slugs if len(slug) != 2 or not slug.isalpha()]
            if invalid:
                preview = ", ".join(invalid[:5])
                raise ValueError(f"CannMenus requires 2-letter state codes. Invalid entries: {preview}")

        return slugs

    def _read_slug_file(self, path: Path) -> List[str]:
        if not path.exists():
            raise FileNotFoundError(f"Missing slug file: {path.name}")
        lines = [
            line.strip().lower().replace(" ", "-")
            for line in path.read_text(encoding="utf-8").splitlines()
        ]
        slugs: List[str] = []
        seen = set()
        for line in lines:
            if not line or line.startswith("#"):
                continue
            if line not in seen:
                seen.add(line)
                slugs.append(line)
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
                elif kind == "metrics":
                    _, runs, locations, items = event
                    self.metrics_var.set(f"Runs: {runs} | Locations: {locations} | Items: {items}")
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
        self.start_button.configure(state=tk.NORMAL, text="Start Run")
        self.cancel_button.configure(state=tk.DISABLED)
        self._set_controls_state(locked=False)
        self.progress_text_var.set("Completed" if success else "Stopped")
        self.status_var.set("Idle" if success else "Stopped")

        elapsed_suffix = ""
        if self.run_started_at:
            elapsed = datetime.now() - self.run_started_at
            elapsed_suffix = f" ({str(elapsed).split('.')[0]})"

        self.summary_var.set(summary)
        self._save_settings()
        self._refresh_run_readiness()
        level = "INFO" if success else "WARNING"
        self._append_log(f"{summary}{elapsed_suffix}", level)
        if self.pending_close:
            self.root.destroy()

    def _append_log(self, text: str, level: str) -> None:
        self.log_text.configure(state=tk.NORMAL)
        tag = level if level in {"INFO", "WARNING", "ERROR"} else "INFO"
        self.log_text.insert(tk.END, f"{text}\n", tag)
        if self.autoscroll_var.get():
            self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _clear_log(self) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _set_controls_state(self, locked: bool) -> None:
        state = tk.DISABLED if locked else tk.NORMAL
        for widget in self.config_widgets:
            widget.configure(state=state)
        self._update_slug_mode_ui()
        self._update_source_ui()
        self._refresh_run_readiness()

    def _load_settings(self) -> None:
        if not GUI_SETTINGS_PATH.exists():
            return
        try:
            data = json.loads(GUI_SETTINGS_PATH.read_text(encoding="utf-8"))
        except Exception:
            return

        self.source_var.set(str(data.get("source", self.source_var.get())))
        self.slug_mode_var.set(str(data.get("slug_mode", self.slug_mode_var.get())))
        self.slug_value_var.set(str(data.get("slug_value", self.slug_value_var.get())))
        self.storefronts_var.set(bool(data.get("storefronts", self.storefronts_var.get())))
        self.deliveries_var.set(bool(data.get("deliveries", self.deliveries_var.get())))
        self.fetch_brands_var.set(bool(data.get("fetch_brands", self.fetch_brands_var.get())))
        self.fetch_strains_var.set(bool(data.get("fetch_strains", self.fetch_strains_var.get())))
        self.test_mode_var.set(bool(data.get("test_mode", self.test_mode_var.get())))
        self.concurrent_var.set(bool(data.get("concurrent", self.concurrent_var.get())))
        self.cache_var.set(bool(data.get("cache_enabled", self.cache_var.get())))
        self.optimize_var.set(bool(data.get("optimize_processing", self.optimize_var.get())))
        self.max_workers_var.set(str(data.get("max_workers", self.max_workers_var.get())))
        self.rate_limit_var.set(str(data.get("rate_limit", self.rate_limit_var.get())))
        self.page_size_var.set(str(data.get("page_size", self.page_size_var.get())))

    def _save_settings(self) -> None:
        data = {
            "source": self.source_var.get(),
            "slug_mode": self.slug_mode_var.get(),
            "slug_value": self.slug_value_var.get().strip(),
            "storefronts": self.storefronts_var.get(),
            "deliveries": self.deliveries_var.get(),
            "fetch_brands": self.fetch_brands_var.get(),
            "fetch_strains": self.fetch_strains_var.get(),
            "test_mode": self.test_mode_var.get(),
            "concurrent": self.concurrent_var.get(),
            "cache_enabled": self.cache_var.get(),
            "optimize_processing": self.optimize_var.get(),
            "max_workers": self.max_workers_var.get(),
            "rate_limit": self.rate_limit_var.get(),
            "page_size": self.page_size_var.get(),
        }
        try:
            GUI_SETTINGS_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            return

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

    def _on_close(self) -> None:
        if self.running:
            confirm = messagebox.askyesno(
                "Run in progress",
                "A run is still active. Cancel and close the app?",
            )
            if not confirm:
                return
            self.cancel_requested.set()
            self.pending_close = True
            self.status_var.set("Cancelling")
            return
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    app = CanaDataGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
