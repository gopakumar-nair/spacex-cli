"""
Cache Manager for storing and retrieving JSON data from files.
"""
import json
import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any


class CacheManager:
    """Manages file-based caching for JSON data."""
    
    def __init__(self, cache_path: str):
        self.cache_path = Path(cache_path)
        self.cache_dir = self.cache_path.parent
        self.logger = logging.getLogger(__name__)
    
    def exists(self) -> bool:
        return self.cache_path.exists() and self.cache_path.is_file()
    
    def is_valid(self, refresh: bool = False) -> bool:
        return self.exists() and not refresh
    
    def load(self) -> Optional[List[Dict[str, Any]]]:
        if not self.exists():
            self.logger.debug(f"Cache file does not exist: {self.cache_path}")
            return None
        
        try:
            self.logger.debug(f"Loading cache from: {self.cache_path}")
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.logger.debug(f"Loaded {len(data)} items from cache")
                return data
        except (json.JSONDecodeError, IOError) as e:
            self.logger.debug(f"Error loading cache: {e}")
            return None
    
    def save(self, data: List[Dict[str, Any]]) -> bool:
        try:
            self.logger.debug(f"Saving {len(data)} items to cache: {self.cache_path}")
            # Create directory if it doesn't exist
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.logger.debug("Cache saved successfully")
            return True
        except IOError as e:
            self.logger.debug(f"Error saving cache: {e}")
            return False
    
    def clear(self) -> bool:        
        if not self.exists():
            return True
        
        try:
            self.cache_path.unlink()
            return True
        except IOError:
            return False
