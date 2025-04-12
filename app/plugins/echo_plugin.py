"""
Simple echo plugin for testing
"""
from typing import Dict, List, Optional, Any

from plugins.interface import SessionBotPlugin

class EchoPlugin(SessionBotPlugin):
    def __init__(self):
        self._config = {}

    @property
    def name(self) -> str:
        return "echo"

    @property
    def prefixes(self) -> List[str]:
        return ["/echo"]

    async def initialize(self, config: Dict[str, Any]) -> None:
        self._config = config

    async def handle_message(self, message: str, sender: str, attachments: Optional[List] = None) -> Dict[str, Any]:
        # Strip prefix
        content = message[5:].strip() if message.startswith("/echo") else message
        
        return {
            'content': f"Echo: {content}",
            'attachments': attachments
        }

    async def cleanup(self) -> None:
        pass
