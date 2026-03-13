import concurrent.futures
import threading
import time
import random
import logging
from typing import List, Dict, Any, Callable
from functools import wraps

logger = logging.getLogger(__name__)


def retry_with_backoff(max_retries=3, base_delay=1.0, max_delay=60.0):
    """Decorator for retrying requests with exponential backoff"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e

                    # Exponential backoff with jitter
                    delay = min(base_delay * (2 ** (retries - 1)), max_delay)
                    jitter = random.uniform(0, 0.1 * delay)
                    time.sleep(delay + jitter)

                    logger.warning(
                        f"Retry {retries}/{max_retries} after error: {str(e)}"
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator


class ConcurrentMenuProcessor:
    def __init__(self, max_workers: int = 10, rate_limit: float = 1.0):
        self.max_workers = max_workers
        self.rate_limit = rate_limit  # Minimum seconds between requests
        self.semaphore = threading.Semaphore(max_workers)
        self.last_request_time = 0.0
        self.request_lock = threading.Lock()
        self.results: Dict[str, Any] = {}
        self.errors: List[Dict[str, Any]] = []

    def process_locations(
        self, locations: List[Dict], process_func: Callable
    ) -> Dict[str, Any]:
        """Process multiple locations concurrently"""
        # Reset results and errors for new processing run
        self.results = {}
        self.errors = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Submit all tasks
            future_to_location = {
                executor.submit(
                    self._process_single_location, location, process_func
                ): location
                for location in locations
            }

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_location):
                location = future_to_location[future]
                try:
                    result = future.result()
                    self.results[location["slug"]] = result
                except Exception as exc:
                    self.errors.append({"location": location, "error": str(exc)})
                    logger.error(
                        f"Location {location['slug']} generated an exception: {exc}"
                    )

        return self.results

    def _process_single_location(
        self, location: Dict[str, Any], process_func: Callable
    ) -> Any:
        """Process a single location with rate limiting"""
        with self.semaphore:
            # Rate limiting
            self._wait_for_rate_limit()

            # Process the location
            return process_func(location)

    def _wait_for_rate_limit(self):
        """Implement rate limiting between requests"""
        with self.request_lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time

            if time_since_last < self.rate_limit:
                sleep_time = self.rate_limit - time_since_last
                time.sleep(sleep_time)

            self.last_request_time = time.time()
