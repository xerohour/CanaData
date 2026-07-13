import logging
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pure Python for efficient flattening
    and normalization of nested data structures without Pandas overhead.
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
        logger.info("Starting robust optimized pure Python data processing...")
        
        flat_items = []
        
        for location_id, items in all_menu_items.items():
            for item in items:
                flat_item = {'_location_id': location_id}
                
                # Use an iterative stack for robust deep flattening
                stack = [("", item)]
                while stack:
                    prefix, current_dict = stack.pop()
                    for k, v in current_dict.items():
                        key = f"{prefix}{k}" if prefix else k

                        if isinstance(v, dict):
                            stack.append((f"{key}.", v))
                        elif isinstance(v, list):
                            if v and isinstance(v[0], dict):
                                if len(v) == 1:
                                    stack.append((f"{key}.", v[0]))
                                else:
                                    flat_item[key] = json.dumps(v)
                            else:
                                flat_item[key] = str(v) if v is not None else 'None'
                        elif v is None:
                            flat_item[key] = 'None'
                        else:
                            # Keep native types for robust coercion later
                            if isinstance(v, (int, float, bool)):
                                flat_item[key] = v
                            else:
                                flat_item[key] = str(v)

                flat_items.append(flat_item)

        if not flat_items:
            logger.info("Processed 0 menu items")
            return []

        # Find all unique keys across all flat items
        all_keys = set()
        for item in flat_items:
            all_keys.update(item.keys())
        
        sorted_keys = sorted(list(all_keys))
        
        numeric_keys = [k for k in sorted_keys if any(x in k.lower() for x in ['price', 'amount', 'thc'])]
        
        normalized_items = []
        for item in flat_items:
            norm_item = {}
            for k in sorted_keys:
                val = item.get(k)
                if val is None:
                    norm_item[k] = 'None'
                elif isinstance(val, str) and k in numeric_keys:
                    try:
                        # Attempt type coercion for expected numeric fields
                        if '.' in val:
                            norm_item[k] = float(val)
                        else:
                            norm_item[k] = int(val)
                    except ValueError:
                        # Fallback to string if casting fails
                        norm_item[k] = val
                else:
                    norm_item[k] = val
            normalized_items.append(norm_item)

        logger.info(f"Processed {len(normalized_items)} menu items")
        return normalized_items
