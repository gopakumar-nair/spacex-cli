"""
Launch Data Access layer - orchestrates data fetching from cache or API.
"""
import logging
from typing import Iterator, Dict, Any, Callable, Optional
from .ApiCaller import ApiCaller
from .CacheManager import CacheManager
import config


class LaunchDataAccess:
    """Orchestrates data fetching from cache or API."""
    
    def __init__(self, cache_path: str):
        """
        Initialize launch data access.
        
        Args:
            cache_path: Path to cache file
        """
        self.logger = logging.getLogger(__name__)
        self.cache_manager = CacheManager(cache_path)
        self.api_caller = ApiCaller(
            timeout=config.API_TIMEOUT,
            allowed_retry_count=config.API_ALLOWED_RETRY_COUNT,
            retry_allowed_on_timeout=config.API_RETRY_ALLOWED_ON_TIMEOUT,
            retry_allowed_on_http_codes=config.API_RETRY_ALLOWED_ON_HTTP_CODES
        )
        self.api_url = config.API_URL
    
    def fetch(
        self,
        refresh: bool,
        onError: Callable[[int, str], None]
    ) -> Optional[Iterator[Dict[str, Any]]]:
        """
        Fetch launch data from cache if file exists and refresh is false, else call API.  
        
        Args:
            refresh: If True, bypass cache and fetch from API
            onError: Callback function called with (error_code, error_message) on error (required)
        
        Returns:
            Iterator of launch dictionaries if successful, None if error occurred
        """
        # Try cache first if not refreshing
        if self.cache_manager.is_valid(refresh):
            self.logger.debug("Cache is valid, attempting to load from cache")
            cached_data = self.cache_manager.load()
            if cached_data is not None:
                self.logger.debug("Using cached data")
                def cache_iterator():
                    for item in cached_data:
                        yield item
                return cache_iterator()
            else:
                self.logger.debug("Cache load failed, fetching from API")
        else:
            self.logger.debug("Cache invalid or refresh requested, fetching from API")
        
        # Fetch from API
        self.logger.debug(f"Fetching data from API: {self.api_url}")
        data, error_code, error_message = self.api_caller.fetch(self.api_url)
        
        if error_code:
            onError(error_code, error_message)
            return None
        
        # Save to cache (continue even if save fails)
        if data:
            self.logger.debug(f"Fetched {len(data)} items from API")
            try:
                self.cache_manager.save(data)
            except Exception:
                # Cache save failure should not stop execution
                self.logger.debug("Cache save failed, continuing without cache")
        
        # Return as iterator
        def api_iterator():
            for item in data:
                yield item
        
        return api_iterator()
