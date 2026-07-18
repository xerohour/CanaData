import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pure Python for efficient flattening
    and normalization of nested data structures.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items using pure Python for maximum performance.
        Replaces pandas overhead with fast list comprehensions and dictionary unpacking.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting optimized pure-Python data processing...")
        
        # Collect all items with location info using fast dict unpacking
        items_with_location = [
            {**item, '_location_id': location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]
        
        if not items_with_location:
            return []
            
        # Flatten all items
        flat_items = []
        for item in items_with_location:
            flat_items.append(self._flatten_dictionary_custom(item))
            
        # Normalize data types and collect all keys
        all_keys = set()
        for item in flat_items:
            for k, v in item.items():
                if v is None:
                    item[k] = 'None'

                # Explicitly coerce numeric types for specific fields to avoid breaking string IDs
                k_lower = k.lower()
                if 'price' in k_lower or 'amount' in k_lower or 'thc' in k_lower:
                    try:
                        if '.' in str(v):
                            item[k] = float(v)
                        else:
                            item[k] = int(v)
                    except (ValueError, TypeError):
                        pass

            all_keys.update(item.keys())
            
        # Ensure uniform keys across all dictionaries for clean CSV export
        sorted_keys = sorted(all_keys)
        result = []
        for item in flat_items:
            # Use 'None' string for missing values to maintain compatibility
            result.append({k: item.get(k, 'None') for k in sorted_keys})
            
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
