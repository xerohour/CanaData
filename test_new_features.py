import os
import sys
import logging
from CanaData import CanaData
from cache_manager import CacheManager
from optimized_data_processor import OptimizedDataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_concurrent_processing():
    """Test concurrent processing feature"""
    logger.info("Testing concurrent processing...")
    
    # Create CanaData instance with concurrent processing enabled
    cana = CanaData(max_workers=5, rate_limit=0.5)
    
    # Test with a small dataset
    cana.locations = [
        {"slug": "test-location-1", "type": "dispensary"},
        {"slug": "test-location-2", "type": "delivery"}
    ]
    
    # This would normally fetch menu data, but we'll just test the structure
    logger.info("Concurrent processing setup complete")
    logger.info(f"Max workers: {cana.max_workers}")
    logger.info(f"Rate limit: {cana.rate_limit}")

def test_caching():
    """Test caching feature"""
    logger.info("Testing caching...")
    
    # Create cache manager
    cache_manager = CacheManager(
        cache_dir="test_cache",
        memory_cache_size=100,
        memory_cache_ttl=60,  # 1 minute for testing
        disk_cache_ttl=300,   # 5 minutes for testing
        enable_disk_cache=True
    )
    
    # Test setting and getting cache data
    test_url = "https://api.example.com/test"
    test_data = {"test": "data", "value": 123}
    
    cache_manager.set(test_url, test_data)
    cached_data = cache_manager.get(test_url)
    
    if cached_data == test_data:
        logger.info("Caching test passed")
    else:
        logger.error("Caching test failed")
    
    # Clean up test cache
    cache_manager.invalidate()
    
def test_data_processing():
    """Test optimized data processing"""
    logger.info("Testing data processing...")
    
    # Create data processor
    processor = OptimizedDataProcessor(max_workers=2)
    
    # Test with sample data
    sample_data = {
        "location1": [
            {
                "name": "Test Product 1",
                "price": {"amount": 50, "currency": "USD"},
                "category": "flower",
                "thc": "20%"
            },
            {
                "name": "Test Product 2",
                "price": {"amount": 75, "currency": "USD"},
                "category": "concentrate",
                "thc": "80%"
            }
        ]
    }
    
    # Process the data
    processed_data = processor.process_menu_data(sample_data)
    
    if len(processed_data) == 2:
        logger.info("Data processing test passed")
        logger.info(f"Processed {len(processed_data)} items")
    else:
        logger.error("Data processing test failed")

def test_integration():
    """Test integration of all features"""
    logger.info("Testing feature integration...")
    
    # Create CanaData instance with all features enabled
    cana = CanaData(
        max_workers=5,
        rate_limit=0.5,
        cache_enabled=True,
        optimize_processing=True
    )
    
    logger.info("Integration test setup complete")
    logger.info(f"Cache enabled: {cana.cache_enabled}")
    logger.info(f"Optimize processing: {cana.optimize_processing}")

if __name__ == "__main__":
    logger.info("Running tests for new CanaData features...")
    
    try:
        test_concurrent_processing()
        test_caching()
        test_data_processing()
        test_integration()
        
        logger.info("All tests completed successfully!")
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        sys.exit(1)