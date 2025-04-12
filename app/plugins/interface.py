"""
Base interface for Session bot plugins
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class SessionBotPlugin(ABC):
    """Abstract base class for all Session bot plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def prefixes(self) -> List[str]:
        """List of command prefixes this plugin handles"""
        pass

    @abstractmethod
    async def handle_message(self, message: str, sender: str, attachments: Optional[List] = None) -> Dict[str, Any]:
        """
        Handle an incoming message
        Args:
            message: The message content
            sender: Session ID of sender
            attachments: Optional list of attachments
        Returns:
            Dict containing response data:
            {
                'content': str,  # Response message
                'attachments': list,  # Optional attachments
                'error': str,  # Optional error message
            }
        """
        pass

    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with config
        Args:
            config: Plugin configuration
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup plugin resources"""
        pass
