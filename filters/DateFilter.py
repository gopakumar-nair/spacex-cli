"""
Data filtering utilities for launch data.
"""
import logging
from typing import Iterator, Dict, Any
from datetime import datetime


class DateFilter:
    """Filters launch data based on date criteria."""
    
    def __init__(self, year: int):
        """
        Initialize date filter.
        
        Args:
            year: Year to filter by
        """
        self.year = year
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Initialized DateFilter for year: {year}")
    
    def filter(self, data: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """
        Filter launches by year.
        
        Args:
            data: Iterator of launch dictionaries
        
        Yields:
            Launch dictionaries matching the year
        """
        matched_count = 0
        skipped_count = 0
        self.logger.debug(f"DateFilter, filtering by year: {self.year}")

        for launch in data:
            date_utc = launch.get('date_utc')
            if not date_utc:
                skipped_count += 1
                continue
            
            try:
                # Parse ISO format date (e.g., "2022-01-01T00:00:00.000Z")
                # Handle 'Z' timezone indicator
                date_str = date_utc.replace('Z', '+00:00') if date_utc.endswith('Z') else date_utc
                launch_date = datetime.fromisoformat(date_str)
                if launch_date.year == self.year:
                    matched_count += 1
                    yield launch
            except (ValueError, AttributeError, TypeError):
                # Skip entries with invalid dates
                skipped_count += 1
                continue
        
        self.logger.debug(f"DateFilter matched {matched_count} launches, skipped {skipped_count}")
