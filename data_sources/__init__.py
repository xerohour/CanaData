"""
Data Sources Package for CanaData

This package provides a modular, pluggable architecture for integrating
multiple cannabis data sources (APIs and scrapers) into CanaData.

Usage:
    from data_sources import DataSourceManager

    manager = DataSourceManager()
    manager.auto_register()  # discovers and registers all built-in adapters
    results = manager.fetch("cannmenus", slug="NY")
"""

from data_sources.base import DataSourceBase, DataSourceType
from data_sources.manager import DataSourceManager

__all__ = ["DataSourceBase", "DataSourceType", "DataSourceManager"]
