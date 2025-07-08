from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all properties from cache if available, otherwise fetch from database
    and cache for 1 hour (3600 seconds)
    """
    properties = cache.get('all_properties')
    
    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
    
    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics
    
    Returns:
        dict: Dictionary containing cache metrics including:
            - hits: Number of successful key lookups
            - misses: Number of failed key lookups
            - hit_ratio: Ratio of hits to total lookups
            - total_commands: Total commands processed by Redis
    """
    try:
        # Get the Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis server information
        info = redis_conn.info("stats")
        
        # Extract relevant metrics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_commands = info.get('total_commands_processed', 0)
        
        # Calculate hit ratio (handle division by zero)
        hit_ratio = hits / (hits + misses) if (hits + misses) > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': round(hit_ratio, 4),
            'total_commands': total_commands
        }
        
        # Log the metrics
        logger.info(
            f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, "
            f"Hit Ratio: {hit_ratio:.2%}, Total Commands: {total_commands}"
        )
        
        return metrics
    
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0,
            'total_commands': 0,
            'error': str(e)
        }
    
def get_all_properties():
    """
    Retrieve all properties from cache if available, otherwise fetch from database
    and cache for 1 hour (3600 seconds)
    """
    # Try to get properties from cache
    properties = cache.get('all_properties')
    
    if properties is None:
        # If not in cache, get from database
        properties = Property.objects.all()
        
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties