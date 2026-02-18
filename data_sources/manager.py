"""
DataSourceManager -- registry and dispatcher for pluggable data sources.

Responsibilities:
  * Register / unregister data source adapters by name.
  * Auto-discover built-in adapters shipped with this package.
  * Dispatch fetch requests to the correct adapter.
  * List available sources and their readiness status.
"""

import logging
from typing import Any, Dict, List, Optional, Type

from data_sources.base import DataSourceBase, DataSourceType

logger = logging.getLogger(__name__)


class DataSourceManager:
    """Central hub that CanaData uses to talk to any data source.

    Example::

        mgr = DataSourceManager()
        mgr.auto_register()

        # fetch using a named source
        result = mgr.fetch("cannmenus", slug="NY")

        # list what's registered
        for info in mgr.list_sources():
            print(info)
    """

    def __init__(self) -> None:
        self._sources: Dict[str, DataSourceBase] = {}

    # -- registration -----------------------------------------------------
    def register(self, source: DataSourceBase) -> None:
        """Register an instantiated data source adapter.

        Args:
            source: An instance of a DataSourceBase subclass.

        Raises:
            TypeError: If *source* is not a DataSourceBase subclass.
            ValueError: If a source with the same name is already registered.
        """
        if not isinstance(source, DataSourceBase):
            raise TypeError(
                f"Expected a DataSourceBase instance, got {type(source).__name__}"
            )
        key = source.name.lower()
        if key in self._sources:
            raise ValueError(f"Data source '{key}' is already registered")
        self._sources[key] = source
        logger.info("Registered data source: %s (%s)", source.name, source.source_type.value)

    def unregister(self, name: str) -> None:
        """Remove a previously registered source by name."""
        key = name.lower()
        if key in self._sources:
            del self._sources[key]
            logger.info("Unregistered data source: %s", name)

    def get(self, name: str) -> Optional[DataSourceBase]:
        """Look up a registered source by name (case-insensitive)."""
        return self._sources.get(name.lower())

    # -- auto-discovery ---------------------------------------------------
    def auto_register(self) -> None:
        """Discover and register all built-in adapters.

        This imports the adapter sub-modules that ship with the package
        and registers any that have the required credentials / deps.
        Adapters that are not available (missing tokens, etc.) are
        logged as warnings and skipped.
        """
        # Lazy imports to avoid circular deps and to tolerate missing packages
        adapters: List[Type[DataSourceBase]] = []

        try:
            from data_sources.cannmenus_adapter import CannMenusAdapter
            adapters.append(CannMenusAdapter)
        except ImportError as exc:
            logger.warning("Could not import CannMenusAdapter: %s", exc)

        try:
            from data_sources.leafly_adapter import LeaflyAdapter
            adapters.append(LeaflyAdapter)
        except ImportError as exc:
            logger.warning("Could not import LeaflyAdapter: %s", exc)

        for adapter_cls in adapters:
            try:
                instance = adapter_cls()
                if instance.is_available():
                    self.register(instance)
                else:
                    logger.warning(
                        "Skipping %s -- not available (missing credentials?)",
                        adapter_cls.name,
                    )
            except Exception as exc:
                logger.warning("Failed to instantiate %s: %s", adapter_cls.__name__, exc)

    # -- dispatch ---------------------------------------------------------
    def fetch(self, source_name: str, slug: str) -> Dict[str, Any]:
        """Fetch locations and menus from a named data source.

        This is the main entry point CanaData should call.

        Args:
            source_name: Registered source name (case-insensitive).
            slug: Search identifier forwarded to the adapter.

        Returns:
            Dict with keys: source, locations, menus, total_items.

        Raises:
            KeyError: If *source_name* is not registered.
        """
        source = self.get(source_name)
        if source is None:
            available = ", ".join(self._sources.keys()) or "(none)"
            raise KeyError(
                f"Data source '{source_name}' is not registered. "
                f"Available: {available}"
            )
        return source.fetch_all(slug)

    def fetch_locations(self, source_name: str, slug: str) -> List[Dict[str, Any]]:
        """Fetch only locations (no menus) from a named data source."""
        source = self.get(source_name)
        if source is None:
            raise KeyError(f"Data source '{source_name}' is not registered")
        return source.get_locations(slug)

    def fetch_menu(self, source_name: str, location_id: str) -> List[Dict[str, Any]]:
        """Fetch menu items for a single location from a named data source."""
        source = self.get(source_name)
        if source is None:
            raise KeyError(f"Data source '{source_name}' is not registered")
        return source.get_menu(location_id)

    # -- introspection ----------------------------------------------------
    def list_sources(self) -> List[Dict[str, Any]]:
        """Return metadata about all registered sources."""
        return [
            {
                "name": src.name,
                "type": src.source_type.value,
                "available": src.is_available(),
            }
            for src in self._sources.values()
        ]

    def __contains__(self, name: str) -> bool:
        return name.lower() in self._sources

    def __len__(self) -> int:
        return len(self._sources)

    def __repr__(self) -> str:
        names = ", ".join(self._sources.keys())
        return f"<DataSourceManager sources=[{names}]>"
