import logging
from typing import List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pure python for efficient flattening
    and normalization of nested data structures.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with pure python optimized flattening.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting pure python optimized data processing...")
        
        items_with_location = [
            {**item, '_location_id': location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]
        
        if not items_with_location:
            return []
            
        flat_items = self._fallback_flattening(items_with_location)
        result = self._normalize_data(flat_items)
        
        logger.info(f"Processed {len(result)} menu items")
        return result
    
    def _fallback_flattening(self, items: List[Dict]) -> List[Dict]:
        """
        Fallback to custom flattening using pure python.
        """
        logger.info("Using pure python fallback flattening method")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            batch_size = max(1, len(items) // self.max_workers)
            
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                future = executor.submit(self._flatten_batch, batch)
                futures.append(future)
            
            flattened_batches = [future.result() for future in futures]
        
        all_flattened = []
        for batch in flattened_batches:
            all_flattened.extend(batch)
        
        return all_flattened
    
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
    
    def _normalize_data(self, items: List[Dict]) -> List[Dict]:
        """
        Normalize and clean the flattened data.
        """
        if not items:
            return items

        all_keys = set()
        for item in items:
            all_keys.update(item.keys())

        sorted_keys = sorted(list(all_keys))
        
        normalized_items = []
        for item in items:
            normalized_item = {}
            for key in sorted_keys:
                val = item.get(key, 'None')
                if val is None:
                    normalized_item[key] = 'None'
                    continue

                if isinstance(val, str) and ('price' in key.lower() or 'amount' in key.lower() or 'thc' in key.lower()):
                    try:
                        if '.' in val:
                            normalized_item[key] = float(val)
                        else:
                            normalized_item[key] = int(val)
                    except ValueError:
                        normalized_item[key] = val
                else:
                    normalized_item[key] = val
            normalized_items.append(normalized_item)

        return normalized_items
