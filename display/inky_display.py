"""
InkyPHAT Display Abstraction Layer

This module handles all InkyPHAT-specific hardware operations.
"""

import sys
import os
from pathlib import Path

# Add stubs directory for Windows development
if not os.path.exists('/etc/rpi-issue'):
    stubs_path = Path(__file__).parent.parent / 'stubs'
    if stubs_path.exists():
        sys.path.insert(0, str(stubs_path))

try:
    from inky.auto import auto
except ImportError as e:
    raise ImportError(
        f"Failed to import inky library: {e}. "
        "Please run the setup script to install dependencies."
    )


class InkyDisplay:
    """Abstraction layer for InkyPHAT display hardware"""
    
    # Color constants
    WHITE = 0
    BLACK = 1
    RED = 2
    
    def __init__(self, logger=None):
        """
        Initialize the InkyPHAT display
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger
        self._log_info("Initializing InkyPHAT display...")
        
        try:
            self._display = auto()
            self.width = self._display.width
            self.height = self._display.height
            self.color = getattr(self._display, 'colour', getattr(self._display, 'color', 'black'))
            
            self._log_info(f"Display initialized: {self.width}x{self.height} pixels")
            self._log_info(f"Display color mode: {self.color}")
            
        except Exception as e:
            self._log_error(f"Failed to initialize display: {e}")
            raise
    
    def set_border(self, color):
        """
        Set the border color
        
        Args:
            color: Color value (WHITE, BLACK, or RED)
        """
        self._log_info(f"Setting border color: {color}")
        self._display.set_border(color)
    
    def show(self, image):
        """
        Display an image on the InkyPHAT
        
        Args:
            image: PIL Image object to display
        """
        self._log_info("Updating display...")
        self._display.set_image(image)
        self._display.show()
        self._log_info("Display updated successfully")
    
    def clear(self, color=WHITE):
        """
        Clear the display to a specific color
        
        Args:
            color: Color to clear to (default: WHITE)
        """
        from PIL import Image
        
        self._log_info(f"Clearing display to color {color}...")
        image = Image.new('P', (self.width, self.height), color)
        self.set_border(color)
        self.show(image)
    
    def _log_info(self, message):
        """Log info message"""
        if self.logger:
            self.logger.info(message)
    
    def _log_error(self, message):
        """Log error message"""
        if self.logger:
            self.logger.error(message)
