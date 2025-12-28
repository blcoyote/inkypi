"""
InkyPHAT Display Abstraction Layer

This module handles all InkyPHAT-specific hardware operations.
"""

import sys
import os
import platform
from pathlib import Path


def _is_raspberry_pi():
    """Check if running on Raspberry Pi hardware"""
    # Check multiple indicators for Raspberry Pi
    if os.path.exists('/etc/rpi-issue'):
        return True
    if os.path.exists('/proc/device-tree/model'):
        try:
            with open('/proc/device-tree/model', 'r') as f:
                if 'raspberry pi' in f.read().lower():
                    return True
        except Exception:
            pass
    # Check for ARM architecture (common on RPi)
    machine = platform.machine().lower()
    if machine in ['armv7l', 'aarch64', 'armv6l']:
        return True
    return False


# Add stubs directory ONLY for non-Raspberry Pi development (Windows/Mac/Linux Desktop)
if not _is_raspberry_pi():
    stubs_path = Path(__file__).parent.parent / 'stubs'
    if stubs_path.exists():
        sys.path.insert(0, str(stubs_path))
        print(f"[DEV MODE] Using hardware stubs from: {stubs_path}")

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
            
            # Rotate display 180 degrees for cable positioning
            self._display.h_flip = True
            self._display.v_flip = True
            
            self._log_info(f"Display initialized: {self.width}x{self.height} pixels")
            self._log_info(f"Display color mode: {self.color}")
            self._log_info("Display rotated 180 degrees")
            
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
