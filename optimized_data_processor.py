import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pure Python list comprehensions
    and dictionary operations for efficient flattening and normalization.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with optimized pure Python flattening.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting highly optimized data processing...")
        flattened_items = []
        for location_id, items in all_menu_items.items():
            for item in items:
                item_copy = {**item, '_location_id': location_id}
                flattened_items.append(self._flatten_dictionary_custom(item_copy))

        if not flattened_items:
            return []
            
        all_keys = set()
        for item in flattened_items:
            all_keys.update(item.keys())
        sorted_keys = sorted(all_keys)
        
        numeric_fields = {'price', 'amount', 'thc'}
        num_keys = {k for k in sorted_keys if any(n_field in k.lower() for n_field in numeric_fields)}
        
        normalized_data = []
        template = dict.fromkeys(sorted_keys, None)
        
        for item in flattened_items:
            for k in num_keys.intersection(item.keys()):
                v = item[k]
                if v is not None and v != 'None':
                    try:
                        v = float(v)
                        if v.is_integer():
                            v = int(v)
                        item[k] = v
                    except (ValueError, TypeError):
                        pass
            
            normalized_item = {**template, **item}
            normalized_data.append(normalized_item)
            
        logger.info(f"Processed {len(normalized_data)} menu items")
        return normalized_data
    
    def _flatten_dictionary_custom(self, d: Dict) -> Dict:
        """
        Optimized version of the existing custom flattening algorithm.
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
                        result[key] = str(v) if v else None
                elif v is None:
                    result[key] = None
                else:
                    result[key] = str(v)
            else:
                if len(stack) > 1:
                    keys.pop()
                stack.pop()
        
        return result
