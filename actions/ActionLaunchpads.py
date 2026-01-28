"""
Action handler for 'launchpads' action - groups launches by launchpad.
"""
import logging
from typing import Iterator, Dict, Any
from collections import Counter


class ActionLaunchpads:
    """Handles 'launchpads' action to group launches by launchpad."""
    
    @staticmethod
    def execute(data: Iterator[Dict[str, Any]]) -> str:
        """
        Group launches by launchpad ID and generate report.
        
        Args:
            data: Iterator of launch dictionaries
        
        Returns:
            Formatted result string with launchpad counts
        """
        logger = logging.getLogger(__name__)
        logger.debug("Executing launchpads action")
        
        launchpad_counts = Counter()
        
        for launch in data:
            launchpad = launch.get('launchpad')
            
            if not launchpad:
                launchpad_id = "unknown"
            elif isinstance(launchpad, str):
                launchpad_id = launchpad
            elif isinstance(launchpad, dict):
                launchpad_id = launchpad.get('id', 'unknown')
            else:
                launchpad_id = "unknown"
            
            launchpad_counts[launchpad_id] += 1
        
        logger.debug(f"Found {len(launchpad_counts)} unique launchpads")
        
        # Sort by count descending
        sorted_counts = sorted(
            launchpad_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Format output
        lines = ["launchpadId - count"]
        for launchpad_id, count in sorted_counts:
            lines.append(f"{launchpad_id} - {count}")
        
        return "\n".join(lines)
