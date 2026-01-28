"""
Pipeline for orchestrating data fetching and processing with fluent interface.
"""
import sys
import logging
from typing import Iterator, Dict, Any, Optional, Callable
from data.LaunchDataAccess import LaunchDataAccess
from actions.ActionRegistry import ActionRegistry
from filters.FilterRegistry import FilterRegistry


class Pipeline:
    """Pipeline for processing launch data with fluent interface."""
    
    def __init__(self, cache_path: str):
        self.logger = logging.getLogger(__name__)
        self.data_access = LaunchDataAccess(cache_path=cache_path)
        self.data_iterator: Optional[Iterator[Dict[str, Any]]] = None
        self.result: Optional[str] = None
    
    def fetch_data(self, refresh: bool = False) -> 'Pipeline':
        self.logger.debug(f"Fetching data (refresh={refresh})")
        
        def handle_error(error_code: int, error_message: str):
            self.logger.error("error in processing")
            self.logger.debug(f"Error {error_code}: {error_message}")
            sys.exit(error_code)
        
        data_iterator = self.data_access.fetch(refresh=refresh, onError=handle_error)
        if data_iterator:
            self.data_iterator = data_iterator
            self.logger.debug("Data fetched successfully")
        else:
            # Error already handled by onError callback
            sys.exit(1)
        
        return self
    
    def filter_data(self, filter_name: str, **kwargs) -> 'Pipeline':
        self.logger.debug(f"Applying filter: {filter_name} with args: {kwargs}")
        
        if self.data_iterator is None:
            raise ValueError("Data must be fetched before filtering")
        
        filter_func = FilterRegistry.get_filter(filter_name, **kwargs)
        self.data_iterator = filter_func(self.data_iterator)
        self.logger.debug(f"filter: {filter_name} applied.")
        return self
    
    def perform_action(self, action: str) -> 'Pipeline':
        self.logger.debug(f"Performing action: {action}")
        
        if self.data_iterator is None:
            raise ValueError("Data must be fetched and filtered before performing action")
        
        handler_class = ActionRegistry.get_action(action)
        self.result = handler_class.execute(self.data_iterator)
        self.logger.debug(f"Action {action} completed")
        return self
    
    def print_result(self) -> None:

        if self.result is None:
            raise ValueError("No result to print")
        
        print(self.result)
