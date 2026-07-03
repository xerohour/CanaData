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
        Process all menu items with optimized flattening.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting pure Python optimized data processing...")
        
        # 1. Flatten all items iteratively
        flat_items = [
            self._flatten_dictionary_custom({**item, '_location_id': loc_id})
            for loc_id, items in all_menu_items.items()
            for item in items
        ]
        
        if not flat_items:
            return []
            
        # 2. Extract all unique keys efficiently
        all_keys = sorted(list(set().union(*(d.keys() for d in flat_items))))
        
        # 3. Create a template to fill missing fields with 'None' string
        # (This matches the legacy format exactly for CSV output compatibility)
        template = dict.fromkeys(all_keys, 'None')
        result = [{**template, **item} for item in flat_items]
        
        # 4. Normalize specific numeric columns dynamically
        target_keys = [k for k in all_keys if any(x in k.lower() for x in ('price', 'amount', 'thc'))]
        for item in result:
            for k in target_keys:
                val = item[k]
                if val != 'None' and isinstance(val, str):
                    try:
                        item[k] = float(val) if '.' in val else int(val)
                    except ValueError:
                        pass
        
        logger.info(f"Processed {len(result)} menu items")
        return result
    
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
    
