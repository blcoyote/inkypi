"""
Content Provider - Business Logic

This module contains application-specific logic for data processing and content generation.
"""

from datetime import datetime


class ContentProvider:
    """Provides content for display"""
    
    def __init__(self, logger=None):
        """
        Initialize the content provider
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger
        self._log_info("ContentProvider initialized")
    
    def get_welcome_message(self):
        """
        Get a welcome message
        
        Returns:
            str: Welcome message
        """
        return "InkyPi Display Ready"
    
    def get_current_time(self):
        """
        Get current time formatted for display
        
        Returns:
            str: Formatted time string
        """
        return datetime.now().strftime("%H:%M:%S")
    
    def get_current_date(self):
        """
        Get current date formatted for display
        
        Returns:
            str: Formatted date string
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    def format_temperature(self, temp_celsius):
        """
        Format temperature for display
        
        Args:
            temp_celsius: Temperature in Celsius
            
        Returns:
            str: Formatted temperature string
        """
        return f"{temp_celsius:.1f}°C"
    
    def _log_info(self, message):
        """Log info message"""
        if self.logger:
            self.logger.info(message)
