import logging
from typing import List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using native Python for efficient flattening
    and normalization of nested data structures, avoiding pandas overhead.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with optimized flattening natively.
        """
        logger.info("Starting optimized data processing...")
        
        flat_items = self._flatten_all_items(all_menu_items)
        result = self._normalize_data(flat_items)
        
        logger.info(f"Processed {len(result)} menu items")
        return result
    
    def _flatten_all_items(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Flatten all menu items natively.
        """
        items_with_location = [
            {**item, '_location_id': location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]
        
        if not items_with_location:
            return []
            
        flat_items = self._fallback_flattening(items_with_location)
        return self._handle_remaining_nesting(flat_items)
    
    def _handle_remaining_nesting(self, items: List[Dict]) -> List[Dict]:
        """
        Handle any remaining nested structures.
        """
        nested_keys = {k for item in items for k, v in item.items() if isinstance(v, (dict, list))}
        for item in items:
            for k in nested_keys:
                if k in item:
                    v = item[k]
                    item[k] = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
        return items
    
    def _fallback_flattening(self, items: List[Dict]) -> List[Dict]:
        """
        Flattening using custom batch processing.
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            batch_size = max(1, len(items) // self.max_workers)
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                futures.append(executor.submit(self._flatten_batch, batch))
            
            flattened_batches = [future.result() for future in futures]
        
        return [item for batch in flattened_batches for item in batch]
    
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
        Normalize and clean the flattened data using dict unpacking.
        """
        if not items:
            return []

        all_keys = sorted(list({k for item in items for k in item.keys()}))
        template_dict = dict.fromkeys(all_keys, None)
        
        normalized = []
        for item in items:
            norm_item = {**template_dict, **item}
            for col in all_keys:
                if 'price' in col.lower() or 'amount' in col.lower() or 'thc' in col.lower():
                    val = norm_item[col]
                    if val is not None and val != 'None':
                        try:
                            f_val = float(val)
                            norm_item[col] = int(f_val) if f_val.is_integer() else f_val
                        except (ValueError, TypeError):
                            pass

            for k, v in norm_item.items():
                if v is None:
                    norm_item[k] = 'None'

            normalized.append(norm_item)

        return normalized
