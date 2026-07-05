import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pure python lists for efficient flattening
    and normalization of nested data structures without pandas overhead.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with optimized flattening using pure python lists for maximum speed.
        
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
        
        flat_data = [self._flatten_dictionary_custom(item) for item in items_with_location]
        
        all_keys = set()
        for item in flat_data:
            all_keys.update(item.keys())
        all_keys_sorted = sorted(list(all_keys))
        
        template = {k: 'None' for k in all_keys_sorted}
        result = []
        numeric_cols = [col for col in all_keys_sorted if 'price' in col.lower() or 'amount' in col.lower() or 'thc' in col.lower()]
        
        for item in flat_data:
            for col in numeric_cols:
                if col in item:
                    val = item[col]
                    if isinstance(val, str) and val != 'None':
                        try:
                            if '.' in val:
                                item[col] = float(val)
                            else:
                                item[col] = int(val)
                        except ValueError:
                            pass
            
            result.append({**template, **item})
            
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
