import pandas as pd
import logging
from typing import List, Dict, Any
import json
from concurrent.futures import ThreadPoolExecutor

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
        logger.info("Starting optimized data processing...")
        
        # We replace the pandas logic with pure python dictionary unpacking and list comprehension
        # as it avoids huge type inference and instantiation overheads of pandas DataFrames.
        # This resolves the bottleneck identified during profiling of data normalization.
        
        all_flattened = []
        for location_id, items in all_menu_items.items():
            for item in items:
                item_with_loc = dict(item)
                item_with_loc['_location_id'] = location_id
                all_flattened.append(self._flatten_dictionary_custom(item_with_loc))

        # Get all keys
        all_keys = set()
        for item in all_flattened:
            all_keys.update(item.keys())

        all_keys_list = sorted(list(all_keys))
        
        # We use a template for filling out missing keys with 'None' to match previous pandas fillna behavior
        template = {key: 'None' for key in all_keys_list}
        
        # Identify numeric columns for type coercion based on original pandas logic
        numeric_cols = [col for col in all_keys_list if 'price' in col.lower() or 'amount' in col.lower() or 'thc' in col.lower()]

        result = []
        for item in all_flattened:
            # First, make sure all item keys with real None map to 'None' string to match pandas
            item_no_nulls = {k: ('None' if v is None else v) for k, v in item.items()}

            # Fast dictionary unpacking, filling missings with 'None' string
            normalized_item = {**template, **item_no_nulls}

            # Convert all numeric strings to numeric dynamically just as pd.to_numeric(errors='coerce') does
            for col in numeric_cols:
                val = normalized_item[col]
                if val != 'None':
                    try:
                        # Try converting to float to mimic pd.to_numeric
                        normalized_item[col] = float(val)
                        # If it's an integer, we could cast it, but float is generally safer and what pandas does for mixed data
                    except (ValueError, TypeError):
                        # leave as original if it fails, which handles the errors='coerce' / notna() logic in original
                        pass

            result.append(normalized_item)

        logger.info(f"Processed {len(result)} menu items")
        return result

    def _flatten_all_items(self, all_menu_items: Dict[str, List[Dict]]) -> pd.DataFrame:
        """
        Flatten all menu items using pandas json_normalize for efficiency.
        """
        # Collect all items with location info
        # Using list comprehension for initialization performance
        items_with_location = [
            {**item, '_location_id': location_id}
            for location_id, items in all_menu_items.items()
            for item in items
        ]
        
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
    
    def _handle_remaining_nesting(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle any remaining nested structures that json_normalize couldn't flatten.
        """
        # Identify columns that still contain nested data
        nested_columns = []
        for col in df.columns:
            # Check if any value in column is a dict or list
            # Avoid O(N) dropna() by using first_valid_index
            if df[col].dtype == 'object':
                first_idx = df[col].first_valid_index()
                if first_idx is not None:
                    val = df[col].loc[first_idx]
                    if isinstance(val, pd.Series):
                        val = val.dropna().iloc[0]
                    if isinstance(val, (dict, list)):
                        nested_columns.append(col)
        
        # Flatten nested columns
        for col in nested_columns:
            try:
                # Convert to string representation for nested data
                # Using list comprehension for performance
                df[col] = [json.dumps(x) if isinstance(x, (dict, list)) else str(x) for x in df[col]]
            except Exception as e:
                logger.warning(f"Failed to flatten column {col}: {e}")
                df[col] = df[col].astype(str)
        
        return df
    
    def _fallback_flattening(self, items: List[Dict]) -> pd.DataFrame:
        """
        Fallback to custom flattening if pandas fails.
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
        
        return pd.DataFrame(all_flattened)
    
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
    
    def _normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
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
