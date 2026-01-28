"""
Filter Registry - maps filter names to filter classes.
"""
import logging
from typing import Dict, Callable, Iterator, Type
from .DateFilter import DateFilter
from .StatusFilter import StatusFilter


class FilterRegistry:
    """Registry for mapping filter names to filter classes."""
    
    _filters: Dict[str, Callable] = {
        'by_year': lambda **kwargs: DateFilter(**kwargs).filter,
        'by_year_and_status': lambda **kwargs: StatusFilter(**kwargs).filter,
    }
    
    @classmethod
    def get_filter(cls, filter_name: str, **kwargs) -> Callable[[Iterator], Iterator]:
        logger = logging.getLogger(__name__)
        logger.debug(f"Getting filter: {filter_name} with kwargs: {kwargs}")
        
        if filter_name not in cls._filters:
            raise ValueError(f"Unknown filter: {filter_name}")
        
        filter_method = cls._filters[filter_name]
        return filter_method(**kwargs)
    
    @classmethod
    def register(cls, filter_name: str, filter_func: Callable):
        cls._filters[filter_name] = filter_func
    
    @classmethod
    def list_filters(cls) -> list[str]:
        """List all registered filters."""
        return list(cls._filters.keys())
