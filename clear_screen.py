#!/usr/bin/env python3
"""
InkyPi - Main Entry Point

This is the main entry point for the InkyPi display application.
Initializes the InkyPHAT display and clears it to white.
"""

import sys
import os
import logging
from pathlib import Path

# Add stubs directory for Windows development
if not os.path.exists("/etc/rpi-issue"):
    stubs_path = Path(__file__).parent / "stubs"
    if stubs_path.exists():
        sys.path.insert(0, str(stubs_path))

from PIL import Image

try:
    from inky.auto import auto
except ImportError as e:
    print(f"Error importing inky library: {e}")
    print("Please run setup script to install dependencies.")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class InkyPiApp:
    """Main application class for InkyPi display"""

    def __init__(self):
        """Initialize the InkyPi application"""
        logger.info("Initializing InkyPi application...")

        # Initialize the InkyPHAT display
        try:
            self.display = auto()
            logger.info(f"Display initialized: {self.display.width}x{self.display.height} pixels")
            logger.info(f"Display color: {self.display.colour}")
        except Exception as e:
            logger.error(f"Failed to initialize display: {e}")
            raise

    def clear_to_white(self):
        """Clear the display to white"""
        logger.info("Clearing display to white...")

        # Create a white image
        image = Image.new("P", (self.display.width, self.display.height), 255)

        # Set border to white
        self.display.set_border(self.display.WHITE)

        # Set and show the image
        self.display.set_image(image)
        self.display.show()

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
