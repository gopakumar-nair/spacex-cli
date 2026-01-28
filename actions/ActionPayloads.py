"""
Action handler for 'payloads' action - calculates average payloads per launch.
"""
import logging
from typing import Iterator, Dict, Any


class ActionPayloads:
    """Handles 'payloads' action to calculate average payloads."""
    
    @staticmethod
    def execute(data: Iterator[Dict[str, Any]]) -> str:
        """
        Calculate average payloads per launch.
        
        Args:
            data: Iterator of launch dictionaries
        
        Returns:
            Formatted result string
        """
        logger = logging.getLogger(__name__)
        logger.debug("Executing payloads action")
        
        total_launches = 0
        total_payloads = 0
        
        for launch in data:
            total_launches += 1
            payloads = launch.get('payloads', [])
            
            # Treat missing payloads as zero
            if not payloads:
                payload_count = 0
            else:
                # payloads can be a list of IDs or objects
                payload_count = len(payloads) if isinstance(payloads, list) else 0
            
            total_payloads += payload_count
        
        logger.debug(f"Payload stats - Launches: {total_launches}, Total payloads: {total_payloads}")
        
        if total_launches > 0:
            average = total_payloads / total_launches
            return f"Average Payload per launch: {average:.2f}"
        else:
            return "Average Payload per launch: 0.00"
