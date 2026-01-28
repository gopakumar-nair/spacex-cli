"""
Action handler for 'report' action - generates launch statistics.
"""
import logging
from typing import Iterator, Dict, Any


class ActionReport:
    """Handles 'report' action to generate launch statistics."""
    
    @staticmethod
    def execute(data: Iterator[Dict[str, Any]]) -> str:
        """
        Generate report statistics.
        
        Args:
            data: Iterator of launch dictionaries
        
        Returns:
            Formatted report string
        """
        logger = logging.getLogger(__name__)
        logger.debug("Executing report action")
        
        total = 0
        successful = 0
        failed = 0
        unknown = 0
        
        for launch in data:
            total += 1
            success = launch.get('success')
            
            if success is None:
                unknown += 1
            elif success:
                successful += 1
            else:
                failed += 1
        
        logger.debug(f"Report stats - Total: {total}, Successful: {successful}, Failed: {failed}, Unknown: {unknown}")
        
        # Calculate success ratio: success / (total - unknown)
        denominator = total - unknown
        if denominator > 0:
            success_ratio = (successful / denominator) * 100
            success_ratio_str = f"{success_ratio:.0f}%"
        else:
            success_ratio_str = "N/A"
        
        return (
            f"Total: {total} | "
            f"Successful: {successful} | "
            f"Failed: {failed} | "
            f"Unknown(success=none): {unknown} | "
            f"Success ratio: {success_ratio_str}"
        )
