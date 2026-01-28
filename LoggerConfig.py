"""
Centralized logging configuration for SpaceX CLI.
"""
import logging


def setup_logging(verbose: bool = False):
    """
    Configure logging for the entire application.
    
    Args:
        verbose: If True, set log level to DEBUG, otherwise ERROR
    """
    level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )
