"""
Plugin manager for Session bot
"""
import asyncio
import importlib
import logging
import os
import sys
from typing import Dict, List, Optional, Type
import yaml

from plugins.interface import SessionBotPlugin

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self, plugins_dir: str, data_dir: str):
        """
        Initialize the plugin manager
        Args:
            plugins_dir: Directory containing plugin packages
            data_dir: Directory containing configuration and data
        """
        self.plugins_dir = plugins_dir
        self.data_dir = data_dir
        self.plugins: Dict[str, SessionBotPlugin] = {}
        self.prefix_map: Dict[str, str] = {}  # Maps prefixes to plugin names
        self.default_plugin: Optional[str] = None

        # Add plugins directory to Python path
        if self.plugins_dir not in sys.path:
            sys.path.append(self.plugins_dir)

    async def load_plugins(self) -> None:
        """Load all enabled plugins from configuration"""
        config_path = os.path.join(self.data_dir, "plugins.yaml")
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Plugin configuration not found at {config_path}")
            return
        except yaml.YAMLError as e:
            logger.error(f"Error parsing plugin configuration: {e}")
            return

        for plugin_config in config.get('plugins', []):
            if not plugin_config.get('enabled', False):
                continue

            name = plugin_config['name']
            package = plugin_config['package']
            
            try:
                # Import plugin module
                module = importlib.import_module(package)
                
                # Find plugin class (subclass of SessionBotPlugin)
                plugin_class = None
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, SessionBotPlugin) and 
                        attr != SessionBotPlugin):
                        plugin_class = attr
                        break

                if not plugin_class:
                    logger.error(f"No valid plugin class found in {package}")
                    continue

                # Initialize plugin
                plugin = plugin_class()
                await plugin.initialize(plugin_config)
                
                # Register plugin
                self.plugins[name] = plugin
                
                # Map prefixes to plugin
                for prefix in plugin.prefixes:
                    if prefix in self.prefix_map:
                        logger.warning(f"Prefix '{prefix}' already registered to {self.prefix_map[prefix]}, "
                                     f"ignoring for {name}")
                    else:
                        self.prefix_map[prefix] = name

                # Set as default if specified
                if plugin_config.get('default', False):
                    if self.default_plugin:
                        logger.warning(f"Multiple default plugins specified, using {name}")
                    self.default_plugin = name

                logger.info(f"Successfully loaded plugin {name}")

            except Exception as e:
                logger.error(f"Error loading plugin {name}: {e}")
                continue

    async def handle_message(self, message: str, sender: str, attachments: Optional[List] = None) -> Dict:
        """
        Handle an incoming message by routing it to the appropriate plugin
        Args:
            message: Message content
            sender: Session ID of sender
            attachments: Optional list of attachments
        Returns:
            Response from plugin
        """
        # Find matching plugin based on prefix
        target_plugin = None
        
        # Check for prefix match
        for prefix, plugin_name in self.prefix_map.items():
            if message.startswith(prefix):
                target_plugin = self.plugins[plugin_name]
                break
        
        # Use default plugin if no prefix match and default exists
        if not target_plugin and self.default_plugin:
            target_plugin = self.plugins[self.default_plugin]

        if not target_plugin:
            return {
                'content': "No plugin found to handle this message",
                'error': "No matching plugin"
            }

        try:
            return await target_plugin.handle_message(message, sender, attachments)
        except Exception as e:
            logger.error(f"Error in plugin while handling message: {e}")
            return {
                'content': "An error occurred while processing your message",
                'error': str(e)
            }

    async def cleanup(self) -> None:
        """Cleanup all plugins"""
        for plugin in self.plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up plugin {plugin.name}: {e}")
