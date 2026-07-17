import logging
from typing import List, Dict, Any
import json

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
        Process all menu items with optimized pure Python flattening.
        """
        logger.info("Starting optimized data processing...")
        flat_items = self._flatten_all_items(all_menu_items)
        result = self._normalize_data(flat_items)
        logger.info(f"Processed {len(result)} menu items")
        return result
    
    def _flatten_all_items(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Flatten all menu items using list comprehensions and dict unpacking.
        """
        items_with_location = [
            {**item, '_location_id': location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]
        
        if not items_with_location:
            return []
            
        all_flattened = []
        for item in items_with_location:
            all_flattened.append(self._flatten_dictionary_custom(item))

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
        Normalize and clean the flattened data using pure Python.
        """
        if not items:
            return []

        all_keys = set()
        for item in items:
            all_keys.update(item.keys())

        template = {k: None for k in sorted(all_keys)}
        
        normalized = []
        for item in items:
            clean_item = {**template, **item}

            for k, v in clean_item.items():
                if clean_item[k] is None:
                    clean_item[k] = 'None'
                elif isinstance(v, str):
                    lower_k = k.lower()
                    if 'price' in lower_k or 'amount' in lower_k or 'thc' in lower_k:
                        try:
                            if '.' in v:
                                clean_item[k] = float(v)
                            else:
                                clean_item[k] = int(v)
                        except (ValueError, TypeError):
                            pass
            normalized.append(clean_item)

        return normalized
