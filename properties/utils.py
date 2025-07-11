import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics including hits, misses, and hit ratio.
    
    Returns:
        dict: Dictionary containing cache metrics
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO command output
        info = redis_conn.info()
        
        # Extract cache stats
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        
        # Calculate hit ratio with explicit conditional
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio,
            'total_requests': total_requests
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2%}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0,
            'total_requests': 0,
            'error': str(e)
        }
        