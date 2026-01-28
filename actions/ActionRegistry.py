"""
Action Registry - maps action strings to action handlers.
"""
import logging
from typing import Dict, Type, Callable
from .ActionReport import ActionReport
from .ActionPayloads import ActionPayloads
from .ActionLaunchpads import ActionLaunchpads


class ActionRegistry:
    """Registry for mapping action names to handlers."""
    
    _actions: Dict[str, Callable[[], str]] = {
        'report': lambda: ActionReport,
        'payloads': lambda: ActionPayloads,
        'launchpads': lambda: ActionLaunchpads,
    }
    
    @classmethod
    def get_action(cls, action: str):
        """
        Get action handler class for given action.
        
        Args:
            action: Action name
        
        Returns:
            Action handler class
        
        Raises:
            ValueError: If action is not registered
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"Getting action handler for: {action}")
        
        if action not in cls._actions:
            raise ValueError(f"Unknown action: {action}")
        
        return cls._actions[action]()
    
    @classmethod
    def register(cls, action: str, handler_class: Type):
        """
        Register a new action handler.
        
        Args:
            action: Action name
            handler_class: Action handler class
        """
        cls._actions[action] = lambda: handler_class
    
    @classmethod
    def list_actions(cls) -> list[str]:
        """List all registered actions."""
        return list(cls._actions.keys())
