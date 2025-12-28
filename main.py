#!/usr/bin/env python3
"""
InkyPi - Main Entry Point

This is the main entry point for the InkyPi display application.
Demonstrates proper separation of concerns with layered architecture.
"""

import sys

# Import from organized layers
from display import InkyDisplay
from rendering import Renderer
from core import ContentProvider
from utils import setup_logger, Config

# Setup logging
logger = setup_logger(__name__)


class InkyPiApp:
    """Main application class demonstrating separation of concerns"""
    
    def __init__(self):
        """Initialize the InkyPi application with dependency injection"""
        logger.info("Initializing InkyPi application...")
        
        # Initialize layers with dependency injection
        self.display = InkyDisplay(logger=logger)
        self.renderer = Renderer(
            width=self.display.width,
            height=self.display.height,
            logger=logger
        )
        self.content = ContentProvider(logger=logger)
        
        logger.info("All layers initialized successfully")
    
    def clear_to_white(self):
        """Clear the display to white"""
        logger.info("Clearing display to white...")
        self.display.clear(color=InkyDisplay.WHITE)
        logger.info("Display cleared to white successfully")
    
    def run(self):
        """Main application run method"""
        logger.info("Running InkyPi application...")
        
        # Clear display to white
        self.clear_to_white()
        
        logger.info("Application completed successfully")


def main():
    """Main entry point"""
    try:
        # Create and run the application
        app = InkyPiApp()
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
