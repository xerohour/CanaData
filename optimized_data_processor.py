import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pure Python for efficient flattening
    and normalization of nested data structures without pandas overhead.
    """
    
    def __init__(self, max_workers: int = 4):
        # max_workers kept for backward compatibility but not used in single-pass
        self.max_workers = max_workers
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with optimized single-pass flattening.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting optimized pure Python data processing...")
        
        flattened_items = []
        all_keys = set()
        
        for location_id, items in all_menu_items.items():
            for item in items:
                result = {'_location_id': location_id}
                stack = [('', item)]
                
                while stack:
                    prefix, curr = stack.pop()
                    if isinstance(curr, dict):
                        for k, v in curr.items():
                            stack.append((f"{prefix}{k}." if prefix else f"{k}.", v))
                    elif isinstance(curr, list):
                        if curr and isinstance(curr[0], dict):
                            if len(curr) == 1:
                                stack.append((prefix, curr[0]))
                            else:
                                result[prefix.rstrip('.')] = json.dumps(curr)
                        else:
                            result[prefix.rstrip('.')] = str(curr) if curr else None
                    else:
                        key = prefix.rstrip('.')
                        # Type coercion constraint (numeric only for price, amount, thc)
                        if curr is not None and any(x in key.lower() for x in ('price', 'amount', 'thc')):
                            try:
                                result[key] = float(curr)
                            except (ValueError, TypeError):
                                result[key] = curr
                        else:
                            result[key] = str(curr) if curr is not None else None

                all_keys.update(result.keys())
                flattened_items.append(result)

        # Normalize: ensure all keys are present and sorted
        sorted_keys = sorted(list(all_keys))
        normalized_data = []
        for item in flattened_items:
            normalized_item = {k: item.get(k, None) for k in sorted_keys}
            normalized_data.append(normalized_item)

        logger.info(f"Processed {len(normalized_data)} menu items")
        return normalized_data
