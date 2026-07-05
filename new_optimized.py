import logging
from typing import List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using native Python for efficient flattening
    and normalization of nested data structures.
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with optimized flattening.

        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items

        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting optimized data processing...")

        items_with_location = [
            {**item, '_location_id': location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]

        if not items_with_location:
            return []

        flattened_items = self._flatten_all_items(items_with_location)
        normalized_data = self._normalize_data(flattened_items)

        logger.info(f"Processed {len(normalized_data)} menu items")
        return normalized_data

    def _flatten_all_items(self, items: List[Dict]) -> List[Dict]:
        """
        Flatten all menu items efficiently.
        """
        # Process in parallel batches
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            batch_size = max(1, len(items) // self.max_workers)

            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                future = executor.submit(self._flatten_batch, batch)
                futures.append(future)

            # Collect results
            flattened_batches = [future.result() for future in futures]

        # Combine all batches
        all_flattened = []
        for batch in flattened_batches:
            all_flattened.extend(batch)

        return all_flattened

    def _flatten_batch(self, batch: List[Dict]) -> List[Dict]:
        """
        Flatten a batch of items using the custom algorithm.
        """
        return [self._flatten_dictionary_custom(item) for item in batch]

    def _flatten_dictionary_custom(self, d: Dict) -> Dict:
        """
        Optimized custom flattening algorithm.
        """
        result = {}
        stack = [iter(d.items())]
        keys = []

        while stack:
            for k, v in stack[-1]:
                key = '.'.join(keys + [k]) if keys else k

                if isinstance(v, dict):
                    keys.append(k)
                    stack.append(iter(v.items()))
                    break
                elif isinstance(v, list):
                    if v and isinstance(v[0], dict):
                        if len(v) == 1:
                            nested_dict = {f"{k}.{sub_k}": sub_v for sub_k, sub_v in v[0].items()}
                            result.update(nested_dict)
                        else:
                            result[key] = json.dumps(v)
                    else:
                        result[key] = str(v) if v else 'None'
                elif v is None:
                    result[key] = 'None'
                else:
                    result[key] = str(v)
            else:
                if len(stack) > 1:
                    keys.pop()
                stack.pop()

        return result

    def _normalize_data(self, data: List[Dict]) -> List[Dict]:
        """
        Normalize and clean the flattened data.
        """
        if not data:
            return []

        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        all_keys = sorted(list(all_keys))

        normalized = []
        for item in data:
            norm_item = {}
            for k in all_keys:
                val = item.get(k, 'None')
                k_lower = k.lower()

                if val != 'None' and ('price' in k_lower or 'amount' in k_lower or 'thc' in k_lower):
                    try:
                        val = float(val) if '.' in str(val) else int(val)
                    except (ValueError, TypeError):
                        pass

                norm_item[k] = val
            normalized.append(norm_item)

        return normalized
