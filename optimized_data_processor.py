import json
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pandas for efficient flattening
    and normalization of nested data structures.
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_menu_data(
        self, all_menu_items: dict[str, list[dict]]
    ) -> list[dict[str, Any]]:
        """
        Process all menu items with optimized flattening using pure Python
        to avoid Pandas DataFrame object allocation overhead.

        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items

        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting optimized data processing (pure Python)...")

        # 1. Flatten all items with location info directly
        items_with_location = [
            {**item, "_location_id": location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]

        if not items_with_location:
            return []

        # 2. Flatten nested dictionaries/lists in batches for parallelism
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            batch_size = max(1, len(items_with_location) // self.max_workers)

            for i in range(0, len(items_with_location), batch_size):
                batch = items_with_location[i : i + batch_size]
                future = executor.submit(self._flatten_batch, batch)
                futures.append(future)

            flat_items = []
            for future in futures:
                flat_items.extend(future.result())

        # 3. Get all unique keys safely without dictionary update overhead
        all_keys = set().union(*(item.keys() for item in flat_items))
        sorted_keys = sorted(all_keys)

        # 4. Normalize and ensure consistent keys
        result = []
        for item in flat_items:
            normalized_item = {}
            for k in sorted_keys:
                v = item.get(k, "None")
                if v is None or v == "":
                    v = "None"

                # Replicate numeric string coercion for specific keys
                if "price" in k.lower() or "amount" in k.lower() or "thc" in k.lower():
                    if isinstance(v, (int, float)):
                        pass
                    elif isinstance(v, str) and v != "None":
                        try:
                            v_float = float(v)
                            v = int(v_float) if v_float.is_integer() else v_float
                        except ValueError:
                            pass
                elif type(v) is bool:
                    v = str(v)

                normalized_item[k] = v
            result.append(normalized_item)

        logger.info(f"Processed {len(result)} menu items")
        return result

    def _flatten_batch(self, batch: list[dict]) -> list[dict]:
        """
        Flatten a batch of items using the existing custom algorithm.
        """
        flattened_items = []
        for item in batch:
            flattened = self._flatten_dictionary_custom(item)
            flattened_items.append(flattened)
        return flattened_items

    def _flatten_dictionary_custom(self, d: dict) -> dict:
        """
        Optimized version of the existing custom flattening algorithm.
        """
        result = {}
        stack = [iter(d.items())]
        keys = []

        # Local bindings for inner loop performance
        _dict = dict
        _list = list
        _dumps = json.dumps
        _isinstance = isinstance

        while stack:
            for k, v in stack[-1]:
                key = ".".join(keys + [k]) if keys else k

                if _isinstance(v, _dict):
                    if not v:
                        result[key] = "None"
                    else:
                        keys.append(k)
                        stack.append(iter(v.items()))
                        break
                elif _isinstance(v, _list):
                    if v and _isinstance(v[0], _dict):
                        result[key] = _dumps(v)
                    else:
                        if v == []:
                            result[key] = "[]"
                        else:
                            result[key] = _dumps(v) if v else "None"
                elif v is None or (hasattr(pd, "NA") and v is pd.NA):
                    result[key] = "None"
                elif v == "":
                    result[key] = "None"
                else:
                    result[key] = v
            else:
                if len(stack) > 1:
                    keys.pop()
                stack.pop()

        return result
