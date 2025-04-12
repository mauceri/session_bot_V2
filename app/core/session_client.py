"""
Core Session client implementation using session-pysdk
"""
import asyncio
import logging
from typing import Optional, Callable, Any, Dict
import asyncio
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class SessionClient:
    def __init__(self, mnemonic: Optional[str] = None):
        """
        Initialize the Session client (Mock version for testing)
        Args:
            mnemonic: Optional mnemonic for restoring existing session
        """
        self._message_handlers: Dict[str, Callable] = {}
        self._mnemonic = mnemonic
        self._session_id = None

    async def start(self):
        """Start the Session client (Mock version)"""
        if not self._mnemonic:
            # Generate a mock mnemonic
            self._mnemonic = 'test mnemonic ' + datetime.now().isoformat()
        
        # Generate a mock session ID
        self._session_id = 'mock_session_' + datetime.now().strftime('%Y%m%d%H%M%S')
        logger.info(f"Mock Session ID: {self._session_id}")
        
        # Start a background task to simulate incoming messages
        asyncio.create_task(self._simulate_messages())

    async def stop(self):
        """Stop the Session client (Mock version)"""
        logger.info("Stopping mock Session client")
        
    async def _simulate_messages(self):
        """Simulate incoming messages for testing"""
        while True:
            await asyncio.sleep(10)  # Simulate a message every 10 seconds
            test_message = f"Test message at {datetime.now().isoformat()}"
            test_sender = "mock_sender_123"
            
            # Call handlers
            for handler in self._message_handlers.values():
                await handler(test_message, test_sender)

    def register_handler(self, prefix: str, handler: Callable):
        """
        Register a message handler for a specific prefix
        Args:
            prefix: Message prefix to handle
            handler: Async callback function
        """
        self._message_handlers[prefix] = handler

    async def send_message(self, recipient: str, content: str, attachments: Optional[list] = None):
        """
        Send a message to a Session recipient (Mock version)
        Args:
            recipient: Session ID of recipient
            content: Message content
            attachments: Optional list of attachments
        """
        logger.info(f"Mock sending message to {recipient}: {content}")
        if attachments:
            logger.info(f"With attachments: {json.dumps(attachments)}")
