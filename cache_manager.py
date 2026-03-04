import time
import json
import hashlib
from typing import Any, Optional, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Multi-tier caching system for API responses and processed data.
    
    Cache Tiers:
    1. Memory Cache (TTL-based) - Fast access for recent data
    2. Disk Cache (File-based) - Persistent storage across runs
    3. Session Cache (In-memory) - Current session data
    """
    
    def __init__(self,
                 cache_dir: str = "cache",
                 memory_cache_size: int = 1000,
                 memory_cache_ttl: int = 3600,  # 1 hour
                 disk_cache_ttl: int = 86400,   # 24 hours
                 enable_disk_cache: bool = True):
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Memory cache with TTL
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.memory_cache_size = max(1, memory_cache_size)
        self.memory_cache_ttl = memory_cache_ttl
        
        # Disk cache settings
        self.disk_cache_ttl = disk_cache_ttl
        self.enable_disk_cache = enable_disk_cache
        
        # Cache statistics
        self.stats = {
            'memory_hits': 0,
            'memory_misses': 0,
            'disk_hits': 0,
            'disk_misses': 0,
            'api_requests': 0
        }
    
    def _generate_cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """Generate a unique cache key for the request"""
        cache_string = url
        if params:
            # Sort params for consistent key generation
            sorted_params = sorted(params.items())
            cache_string += "?" + "&".join(f"{k}={v}" for k, v in sorted_params)
        
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Retrieve data from cache"""
        cache_key = self._generate_cache_key(url, params)
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if time.time() - entry['timestamp'] < self.memory_cache_ttl:
                self.stats['memory_hits'] += 1
                entry['timestamp'] = time.time()
                logger.debug(f"Memory cache hit for {url}")
                return entry['data']
            else:
                # Remove expired entry
                self.memory_cache.pop(cache_key, None)
        
        self.stats['memory_misses'] += 1
        
        # Check disk cache if enabled
        if self.enable_disk_cache:
            disk_data = self._get_from_disk(cache_key)
            if disk_data is not None:
                self.stats['disk_hits'] += 1
                # Load back into memory cache
                self.memory_cache[cache_key] = {
                    'data': disk_data,
                    'timestamp': time.time()
                }
                self._prune_memory_cache()
                logger.debug(f"Disk cache hit for {url}")
                return disk_data
        
        self.stats['disk_misses'] += 1
        return None
    
    def set(self, url: str, data: Any, params: Optional[Dict] = None) -> None:
        """Store data in cache"""
        cache_key = self._generate_cache_key(url, params)
        
        # Store in memory cache
        self.memory_cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        self._prune_memory_cache()
        
        # Store in disk cache if enabled
        if self.enable_disk_cache:
            self._set_to_disk(cache_key, data)

    def _prune_memory_cache(self) -> None:
        """Enforce memory cache size using oldest-entry eviction."""
        while len(self.memory_cache) > self.memory_cache_size:
            oldest_key = min(self.memory_cache, key=lambda key: self.memory_cache[key]['timestamp'])
            self.memory_cache.pop(oldest_key, None)
    
    def _get_from_disk(self, cache_key: str) -> Optional[Any]:
        """Retrieve data from disk cache"""
        cache_file = self.cache_dir / f"{cache_key}.json_cache"
        
        if not cache_file.exists():
            return None
        
        try:
            # Check if cache is expired
            file_time = cache_file.stat().st_mtime
            if time.time() - file_time > self.disk_cache_ttl:
                cache_file.unlink()  # Remove expired cache
                return None
            
            # Load cached data
            with open(cache_file, 'r') as f:
                return json.load(f)
                
        except (json.JSONDecodeError, EOFError, FileNotFoundError) as e:
            logger.warning(f"Failed to load cache file {cache_file}: {e}")
            return None
    
    def _set_to_disk(self, cache_key: str, data: Any) -> None:
        """Store data in disk cache"""
        cache_file = self.cache_dir / f"{cache_key}.json_cache"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except TypeError as e:
            logger.warning(f"Failed to save cache file {cache_file}: {e}")
    
    def invalidate(self, pattern: Optional[str] = None) -> None:
        """Invalidate cache entries"""
        if pattern:
            # Invalidate entries matching pattern
            keys_to_remove = []
            for key in self.memory_cache.keys():
                if pattern in str(key):
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                self.memory_cache.pop(key, None)
            
            # Remove matching files from disk cache
            for cache_file in self.cache_dir.glob("*.json_cache"):
                if pattern in cache_file.name:
                    cache_file.unlink()
        else:
            # Clear all cache
            self.memory_cache.clear()
            if self.enable_disk_cache:
                for cache_file in self.cache_dir.glob("*.json_cache"):
                    cache_file.unlink()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.stats['memory_hits'] + self.stats['memory_misses']
        hit_rate = 0.0
        if total_requests > 0:
            hit_rate = (self.stats['memory_hits'] + self.stats['disk_hits']) / total_requests * 100
        
        # Convert to string with 2 decimal places to avoid rounding issues
        hit_rate_str = f"{hit_rate:.2f}"
        hit_rate_float = float(hit_rate_str)
        
        return {
            **self.stats,
            'hit_rate_percent': hit_rate_float,
            'memory_cache_size': len(self.memory_cache),
            'disk_cache_files': len(list(self.cache_dir.glob("*.json_cache"))) if self.enable_disk_cache else 0
        }
