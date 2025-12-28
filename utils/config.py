"""
Configuration Management

Application configuration settings and constants.
"""


class Config:
    """Application configuration"""
    
    # Display configuration
    DISPLAY_CONFIG = {
        'width': 250,
        'height': 122,
        'color': 'black',
        'rotation': 0
    }
    
    # Refresh configuration
    REFRESH_CONFIG = {
        'interval': 300,  # seconds
        'force_update': False
    }
    
    # Colors
    WHITE = 0
    BLACK = 1
    RED = 2
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = None  # Set to file path to enable file logging
    
    @classmethod
    def get_display_width(cls):
        """Get display width"""
        return cls.DISPLAY_CONFIG['width']
    
    @classmethod
    def get_display_height(cls):
        """Get display height"""
        return cls.DISPLAY_CONFIG['height']
    
    @classmethod
    def get_refresh_interval(cls):
        """Get refresh interval in seconds"""
        return cls.REFRESH_CONFIG['interval']
