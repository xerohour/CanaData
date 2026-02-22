import logging
from typing import List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    pd = None
    PANDAS_AVAILABLE = False
    logger.warning("Pandas not available. Optimized processing will be disabled.")

class OptimizedDataProcessor:
    """
    Optimized data processing pipeline using pandas for efficient flattening
    and normalization of nested data structures.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        if not PANDAS_AVAILABLE:
            logger.warning("Pandas is not installed. OptimizedDataProcessor will use fallback method.")
    
    def process_menu_data(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Process all menu items with optimized flattening.
        
        Args:
            all_menu_items: Dictionary mapping location IDs to lists of menu items
            
        Returns:
            List of flattened dictionaries ready for CSV export
        """
        logger.info("Starting optimized data processing...")
        
        if not PANDAS_AVAILABLE:
            return self._fallback_process_all(all_menu_items)

        # Convert to DataFrame for batch processing
        flat_items = self._flatten_all_items(all_menu_items)
        
        # Normalize and clean data
        normalized_data = self._normalize_data(flat_items)
        
        # Convert back to list of dictionaries
        result = normalized_data.to_dict('records')
        
        logger.info(f"Processed {len(result)} menu items")
        return result
    
    def _flatten_all_items(self, all_menu_items: Dict[str, List[Dict]]) -> 'pd.DataFrame':
        """
        Flatten all menu items using pandas json_normalize for efficiency.
        """
        # Collect all items with location info
        items_with_location = []
        for location_id, items in all_menu_items.items():
            for item in items:
                item_copy = item.copy()
                item_copy['_location_id'] = location_id
                items_with_location.append(item_copy)
        
        if not items_with_location:
            return pd.DataFrame()
        
        # Use pandas json_normalize for efficient flattening
        try:
            df = pd.json_normalize(items_with_location, sep='.')
            
            # Handle any remaining nested structures
            df = self._handle_remaining_nesting(df)
            
            return df
        except Exception as e:
            logger.warning(f"Pandas normalization failed, falling back to custom method: {e}")
            return self._fallback_flattening(items_with_location)
    
    def _handle_remaining_nesting(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """
        Handle any remaining nested structures that json_normalize couldn't flatten.
        """
        # Identify columns that still contain nested data
        nested_columns = []
        for col in df.columns:
            # Check if any value in column is a dict or list
            sample_values = df[col].dropna().head(10)
            if len(sample_values) > 0:
                if isinstance(sample_values.iloc[0], (dict, list)):
                    nested_columns.append(col)
        
        # Flatten nested columns
        for col in nested_columns:
            try:
                # Convert to string representation for nested data
                df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (dict, list)) else str(x))
            except Exception as e:
                logger.warning(f"Failed to flatten column {col}: {e}")
                df[col] = df[col].astype(str)
        
        return df
    
    def _fallback_process_all(self, all_menu_items: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """
        Complete processing without pandas.
        """
        logger.info("Using fallback processing (No Pandas)")
        items_with_location = []
        for location_id, items in all_menu_items.items():
            for item in items:
                item_copy = item.copy()
                item_copy['_location_id'] = location_id
                items_with_location.append(item_copy)

        # Flatten
        flattened = self._fallback_flattening_list(items_with_location)

        # Normalize
        normalized = self._normalize_data_fallback(flattened)
        return normalized

    def _fallback_flattening(self, items: List[Dict]) -> 'pd.DataFrame':
        """
        Fallback to custom flattening if pandas fails, returns DataFrame.
        """
        flattened_list = self._fallback_flattening_list(items)
        return pd.DataFrame(flattened_list)

    def _fallback_flattening_list(self, items: List[Dict]) -> List[Dict]:
        """
        Fallback to custom flattening returning list of dicts.
        """
        logger.info("Using fallback flattening method")
        
        # Process in parallel batches
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            batch_size = max(1, len(items) // self.max_workers)
            
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                future = executor.submit(self._flatten_batch, batch)
                futures.append(future)
            
            # Collect results
            flattened_batches = [future.result() for future in futures]
        
        # Combine all batches
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
        Optimized version of the custom flattening algorithm.
        """
        result = {}
        # Stack contains tuples of (dictionary, parent_key_prefix)
        stack = [(d, "")]
        
        while stack:
            curr_dict, prefix = stack.pop()

            for k, v in curr_dict.items():
                key = f"{prefix}.{k}" if prefix else k
                
                if isinstance(v, dict):
                    if not v:
                         result[key] = 'None'
                    else:
                         stack.append((v, key))
                elif isinstance(v, list):
                    if v and isinstance(v[0], dict):
                        if len(v) == 1:
                            # Single item list of dict, flatten it
                            # We push it to stack effectively as if it was a dict
                            stack.append((v[0], key))
                        else:
                            # Multiple items, convert to JSON string
                            result[key] = json.dumps(v)
                    else:
                        # Simple list or empty list
                        result[key] = json.dumps(v) if v else 'None'
                elif v is None:
                    result[key] = 'None'
                else:
                    result[key] = str(v)

        return result
    
    def _normalize_data(self, df: 'pd.DataFrame') -> 'pd.DataFrame':
        """
        Normalize and clean the flattened data.
        """
        if df.empty:
            return df
        
        # Ensure all columns are present and fill missing values
        df = df.fillna('None')
        
        # Convert data types where possible
        for col in df.columns:
            # Try to convert to numeric where possible
            if 'price' in col.lower() or 'amount' in col.lower() or 'thc' in col.lower():
                original_col = df[col]
                numeric_col = pd.to_numeric(original_col, errors='coerce')
                df[col] = numeric_col.where(numeric_col.notna(), original_col)
        
        # Sort columns for consistency
        df = df.reindex(sorted(df.columns), axis=1)
        
        return df

    def _normalize_data_fallback(self, data: List[Dict]) -> List[Dict]:
        """
        Normalize and clean data without pandas.
        """
        if not data:
            return []

        # 1. Collect all keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())

        sorted_keys = sorted(list(all_keys))

        normalized = []
        for item in data:
            new_item = {}
            for key in sorted_keys:
                val = item.get(key, 'None')
                # Basic numeric cleanup if needed, but for CSV strings are fine.
                # If we really want to mimic pandas 'None' behavior for NaNs:
                if val is None:
                    val = 'None'
                new_item[key] = str(val)
            normalized.append(new_item)

        return normalized
