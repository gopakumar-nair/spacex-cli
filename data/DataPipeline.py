"""
Data Pipeline for chaining data processing operations.
"""
from typing import Iterator, Dict, Any, Callable, Optional
from filters.DateFilter import DateFilter
from actions.ActionRegistry import ActionRegistry


class DataPipeline:
    """Pipeline for processing launch data with fluent interface."""
    
    def __init__(self, data_iterator: Iterator[Dict[str, Any]]):
        self.data_iterator = data_iterator
    
    def filter_data(self, filter_func: Callable, *args, **kwargs) -> 'DataPipeline':
        self.data_iterator = filter_func(self.data_iterator, *args, **kwargs)
        return self
    
    def perform_action(self, action: str) -> 'DataPipeline':
        handler_class = ActionRegistry.get_action(action)
        self.result = handler_class.execute(self.data_iterator)
        return self
    
    def print(self) -> None:
        print(self.result)
