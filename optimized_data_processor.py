import pandas as pd
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
        Process all menu items with optimized flattening.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting optimized pure Python data processing...")
        
        # Flatten all items directly
        flat_items = []
        all_keys = set()
        
        for loc_id, items in all_menu_items.items():
            for item in items:
                flat_item = self._flatten_dictionary_custom(item)
                flat_item['_location_id'] = loc_id
                all_keys.update(flat_item.keys())
                flat_items.append(flat_item)

        if not flat_items:
            return []
            
        # Sort keys and create template
        sorted_keys = sorted(list(all_keys))
        template = dict.fromkeys(sorted_keys, None)
        
        # Numeric fields coercion constraints
        numeric_fields = {
            col for col in sorted_keys
            if 'price' in col.lower() or 'amount' in col.lower() or 'thc' in col.lower()
        }
        
        # Normalize and pack using list comprehensions and dictionary unpacking
        result = []
        for item in flat_items:
            normalized = {**template, **item}
            
            # Coerce constrained numeric fields
            for field in numeric_fields:
                val = normalized.get(field)
                if val is not None:
                    try:
                        normalized[field] = float(val) if '.' in str(val) else int(val)
                    except (ValueError, TypeError):
                        pass

            result.append(normalized)
            
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
                        result[key] = str(v) if v else None
                elif v is None:
                    result[key] = None
                else:
                    result[key] = str(v)
            else:
                # Pop from stack when iterator is exhausted
                if len(stack) > 1:
                    keys.pop()
                stack.pop()
        
        return result
