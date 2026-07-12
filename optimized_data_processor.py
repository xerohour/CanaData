import logging
from typing import List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pandas for efficient flattening
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
            
        # Process in parallel batches using pure Python
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            batch_size = max(1, len(items_with_location) // self.max_workers)
            
            for i in range(0, len(items_with_location), batch_size):
                batch = items_with_location[i:i + batch_size]
                future = executor.submit(self._flatten_batch, batch)
                futures.append(future)
            
            # Collect results
            flattened_batches = [future.result() for future in futures]
        
        # Combine all batches
        all_flattened = []
        for batch in flattened_batches:
            all_flattened.extend(batch)

        # Normalize and clean data
        result = self._normalize_data(all_flattened)
        
        logger.info(f"Processed {len(result)} menu items")
        return result
    
    def _flatten_batch(self, batch: List[Dict]) -> List[Dict]:
        """
        Flatten a batch of items using the existing custom algorithm.
        """
        flattened_items = []
        for item in batch:
            flattened = self._flatten_dictionary_custom(item)
            flattened_items.append(flattened)
        return flattened_items
    
    def _flatten_dictionary_custom(self, d: Dict) -> Dict:
        """
        Optimized version of the existing custom flattening algorithm.
        """
        # Pre-allocate result dict with estimated size
        result = {}
        
        # Use iterative approach with explicit stack
        stack = [iter(d.items())]
        keys = []
        
        while stack:
            for k, v in stack[-1]:
                key = '.'.join(keys + [k]) if keys else k
                
                if isinstance(v, dict):
                    # Push nested dict to stack
                    keys.append(k)
                    stack.append(iter(v.items()))
                    break
                elif isinstance(v, list):
                    if v and isinstance(v[0], dict):
                        # Handle list of dicts by taking first item or joining
                        if len(v) == 1:
                            # Single item, flatten it
                            nested_dict = {f"{k}.{sub_k}": sub_v for sub_k, sub_v in v[0].items()}
                            result.update(nested_dict)
                        else:
                            # Multiple items, convert to JSON string
                            result[key] = json.dumps(v)
                    else:
                        # Simple list, convert to string representation
                        result[key] = str(v) if v else 'None'
                elif v is None:
                    result[key] = 'None'
                else:
                    result[key] = str(v)
            else:
                # Pop from stack when iterator is exhausted
                if len(stack) > 1:
                    keys.pop()
                stack.pop()
        
        return result
    
    def _normalize_data(self, flat_items: List[Dict]) -> List[Dict]:
        """
        Normalize and clean the flattened data in pure Python without Pandas overhead.
        """
        if not flat_items:
            return []

        # Determine all unique keys across all items
        keys_set = set()
        for item in flat_items:
            keys_set.update(item.keys())

        sorted_keys = sorted(list(keys_set))
        # Pre-compute template dictionary for O(1) filling, using None as base
        template = dict.fromkeys(sorted_keys, None)
        
        normalized_data = []
        for item in flat_items:
            # Dictionary unpacking with template ensures all keys are present
            normalized_item = {**template, **item}

            # Robust type coercion without hardcoded keys
            for k, v in normalized_item.items():
                if v is not None and isinstance(v, str):
                    # Fast check for potential numeric string to avoid expensive try/except on all strings
                    if v.lstrip('-').replace('.', '', 1).isdigit():
                        try:
                            f = float(v)
                            normalized_item[k] = int(f) if f.is_integer() else f
                        except ValueError:
                            pass

                # Fill missing values with string 'None' to match previous behavior
                if normalized_item[k] is None:
                    normalized_item[k] = 'None'

            normalized_data.append(normalized_item)

        return normalized_data
