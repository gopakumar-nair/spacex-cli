"""
Status filtering utilities for launch data.
"""
import logging
from typing import Iterator, Dict, Any, Optional
from datetime import datetime


class StatusFilter:
    """Filters launch data based on year and status criteria."""
    
    def __init__(self, year: int, status: Optional[bool] = None):
        """
        Initialize status filter.
        
        Args:
            year: Year to filter by
            status: Status to filter by (True=successful, False=failed, None=all statuses)
        """
        self.year = year
        self.status = status
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Initialized StatusFilter for year: {year}, status: {status}")
    
    def filter(self, data: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """
        Filter launches by year and status (success).
        
        Args:
            data: Iterator of launch dictionaries
        
        Yields:
            Launch dictionaries matching the year and status
        """
        matched_count = 0
        skipped_count = 0
        
        for launch in data:
            # Filter by year
            date_utc = launch.get('date_utc')
            if not date_utc:
                skipped_count += 1
                continue
            
            try:
                # Parse ISO format date (e.g., "2022-01-01T00:00:00.000Z")
                # Handle 'Z' timezone indicator
                date_str = date_utc.replace('Z', '+00:00') if date_utc.endswith('Z') else date_utc
                launch_date = datetime.fromisoformat(date_str)
                if launch_date.year != self.year:
                    skipped_count += 1
                    continue
            except (ValueError, AttributeError, TypeError):
                # Skip entries with invalid dates
                skipped_count += 1
                continue
            
            # Filter by status if specified
            if self.status is not None:
                success = launch.get('success')
                if success != self.status:
                    skipped_count += 1
                    continue
            
            matched_count += 1
            yield launch
        
        self.logger.debug(f"StatusFilter matched {matched_count} launches, skipped {skipped_count}")
