"""
Main entry point for Session bot
"""
import asyncio
import logging
import os
from typing import Optional

from core.session_client import SessionClient
from core.plugin_manager import PluginManager

logger = logging.getLogger(__name__)

class SessionBot:
    def __init__(self):
        self.data_dir = os.getenv('DATA_DIR', '/data')
        self.plugins_dir = os.getenv('PLUGINS_DIR', '/plugins')
        
        # Initialize components
        self.session = SessionClient(
            mnemonic=os.getenv('SESSION_BOT_MNEMONIC')
        )
        self.plugin_manager = PluginManager(
            plugins_dir=self.plugins_dir,
            data_dir=self.data_dir
        )

    async def handle_message(self, content: str, sender: str, attachments: Optional[list] = None):
        """Handle incoming Session message"""
        response = await self.plugin_manager.handle_message(content, sender, attachments)
        
        if 'error' in response:
            logger.error(f"Error handling message: {response['error']}")
        
        if 'content' in response:
            await self.session.send_message(
                recipient=sender,
                content=response['content'],
                attachments=response.get('attachments')
            )

    async def start(self):
        """Start the bot"""
        # Initialize Session client
        await self.session.start()
        
        # Load plugins
        await self.plugin_manager.load_plugins()
        
        # Register message handler
        self.session.register_handler('', self.handle_message)  # Empty prefix to handle all messages
        
        logger.info("Bot started successfully")
        
        # Keep the bot running
        while True:
            await asyncio.sleep(1)

    async def cleanup(self):
        """Cleanup resources"""
        await self.plugin_manager.cleanup()
        await self.session.stop()

async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    bot = SessionBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await bot.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
