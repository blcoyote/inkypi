# InkyPHAT Raspberry Pi Project Instructions

## Project Overview

This is a Raspberry Pi Python project utilizing an InkyPHAT 2.13" EPD (E-Paper Display) with the following specifications:
- **Display Size**: 2.13 inches
- **Resolution**: 250x122 pixels
- **Colors**: Black and White
- **Technology**: E-Paper Display (EPD)

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Pimoroni InkyPHAT 2.13" display
- Power supply for Raspberry Pi

## Software Dependencies

### System Requirements
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy
```

### Python Libraries
```bash
pip3 install inky[rpi,example-depends]
# or minimal installation:
pip3 install inky pillow
```

## Display Specifications

- **Width**: 250 pixels
- **Height**: 122 pixels
- **Refresh Rate**: ~15 seconds (typical for E-Paper)
- **Power Consumption**: Very low (only during refresh)
- **Viewing Angle**: 180°
- **Note**: E-Paper displays retain image without power

## Code Practices and Separation of Concerns

### Architecture Principles

This project follows clean code principles to maintain readability, testability, and maintainability. The codebase should be organized with clear separation of concerns:

#### 1. **Display Layer** (`display/`)
Handles all InkyPHAT-specific operations:
- Display initialization and configuration
- Low-level drawing operations
- Screen refresh and update logic
- Hardware abstraction

**Example structure:**
```python
# display/inky_display.py
class InkyDisplay:
    def __init__(self):
        """Initialize InkyPHAT display"""
        
    def clear(self):
        """Clear the display"""
        
    def show(self, image):
        """Render image to display"""
        
    def draw_text(self, text, position, font_size):
        """Draw text at position"""
```

#### 2. **Business Logic Layer** (`core/`)
Contains application-specific logic independent of display hardware:
- Data processing
- Content generation
- API integrations
- Scheduling logic

**Example structure:**
```python
# core/content_provider.py
class ContentProvider:
    def get_weather_data(self):
        """Fetch weather information"""
        
    def get_calendar_events(self):
        """Retrieve calendar events"""
        
    def format_data(self, data):
        """Format data for display"""
```

#### 3. **Rendering Layer** (`rendering/`)
Bridges business logic and display layer:
- Image composition
- Layout management
- Font handling
- Drawing operations on PIL Image objects

**Example structure:**
```python
# rendering/renderer.py
class Renderer:
    def create_image(self, width, height):
        """Create blank PIL Image"""
        
    def compose_layout(self, data):
        """Arrange data elements on image"""
        
    def apply_styling(self, image, style):
        """Apply visual styling"""
```

#### 4. **Utilities** (`utils/`)
Helper functions and shared utilities:
- Configuration management
- Logging setup
- Date/time formatting
- File operations

**Example structure:**
```python
# utils/config.py
def load_config(config_file):
    """Load configuration from file"""
    
# utils/logger.py
def setup_logger(name, level):
    """Configure application logger"""
```

### Best Practices

#### Code Organization
1. **One class per file** for main components
2. **Group related functions** into modules
3. **Use descriptive names** that reflect purpose
4. **Keep functions small** (single responsibility)
5. **Avoid deep nesting** (max 3-4 levels)

#### E-Paper Display Considerations
```python
# GOOD: Minimize refreshes (e-paper has limited refresh cycles)
def update_display_if_changed(new_content):
    if new_content != current_content:
        display.show(new_content)
        
# BAD: Frequent unnecessary refreshes
def update_display_continuously():
    while True:
        display.show(content)  # Wears out display
        time.sleep(1)
```

#### Error Handling
```python
# Display layer should handle hardware errors
try:
    inky.show()
except InkyException as e:
    logger.error(f"Display error: {e}")
    # Fallback behavior
    
# Business logic should handle data errors
try:
    data = fetch_weather()
except APIError as e:
    logger.error(f"API error: {e}")
    return default_data()
```

#### Dependency Injection
```python
# GOOD: Inject dependencies
class WeatherDisplay:
    def __init__(self, display, weather_service):
        self.display = display
        self.weather_service = weather_service
        
# BAD: Hard-coded dependencies
class WeatherDisplay:
    def __init__(self):
        self.display = InkyDisplay()  # Tight coupling
        self.weather_service = WeatherAPI()  # Hard to test
```

#### Configuration Management
```python
# config.py
DISPLAY_CONFIG = {
    'width': 250,
    'height': 122,
    'color': 'black',
    'rotation': 0
}

REFRESH_CONFIG = {
    'interval': 300,  # seconds
    'force_update': False
}

# Use constants instead of magic numbers
from config import DISPLAY_CONFIG

width = DISPLAY_CONFIG['width']  # GOOD
width = 250  # BAD (magic number)
```

### Testing Strategy

#### Unit Tests
- Test business logic independently
- Mock display hardware for testing
- Verify data transformations

```python
# tests/test_content_provider.py
def test_format_temperature():
    provider = ContentProvider()
    result = provider.format_temperature(22.5)
    assert result == "22.5°C"
```

#### Integration Tests
- Test display rendering with mock hardware
- Verify image generation
- Check layout composition

#### Hardware Tests
- Run on actual Raspberry Pi with InkyPHAT
- Verify display updates correctly
- Test error recovery

## Project Structure Example

```
inkypi/
├── display/
│   ├── __init__.py
│   └── inky_display.py       # Display abstraction
├── core/
│   ├── __init__.py
│   ├── content_provider.py   # Business logic
│   └── scheduler.py          # Update scheduling
├── rendering/
│   ├── __init__.py
│   ├── renderer.py           # Image composition
│   └── layouts.py            # Layout templates
├── utils/
│   ├── __init__.py
│   ├── config.py             # Configuration
│   └── logger.py             # Logging setup
├── fonts/                    # Font files
├── assets/                   # Images, icons
├── tests/
│   ├── test_display.py
│   ├── test_content.py
│   └── test_rendering.py
├── main.py                   # Application entry point
├── config.json               # Configuration file
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Running the Project

### Development Mode
```bash
python3 main.py --debug
```

### Production Mode
```bash
python3 main.py
```

### Auto-start on Boot
Add to `/etc/rc.local` (before `exit 0`):
```bash
/usr/bin/python3 /home/pi/inkypi/main.py &
```

Or create a systemd service:
```bash
sudo nano /etc/systemd/system/inkypi.service
```

```ini
[Unit]
Description=InkyPHAT Display Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/inkypi/main.py
WorkingDirectory=/home/pi/inkypi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl enable inkypi.service
sudo systemctl start inkypi.service
```

## Common Pitfalls

1. **Over-refreshing**: E-paper displays have limited refresh cycles (~1 million). Update only when content changes.
2. **Blocking operations**: Fetch data asynchronously to avoid freezing the display update loop.
3. **Image retention**: Clear the display periodically to prevent ghosting.
4. **Color modes**: InkyPHAT supports black/white only - dithering may be needed for grayscale.
5. **GPIO conflicts**: Ensure no other processes are using the SPI interface.

## Debugging Tips

```bash
# Check if InkyPHAT is detected
ls /dev/spidev*

# Enable SPI if needed
sudo raspi-config
# Interface Options -> SPI -> Enable

# Test display with example
python3 -c "from inky.auto import auto; inky = auto(); inky.set_border(inky.BLACK); inky.show()"

# Check logs
tail -f /var/log/inkypi.log
```

## Resources

- [Pimoroni InkyPHAT Documentation](https://learn.pimoroni.com/article/getting-started-with-inky-phat)
- [Inky Python Library](https://github.com/pimoroni/inky)
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [E-Paper Best Practices](https://www.waveshare.com/wiki/E-Paper_Driver_HAT)

## License

MIT License
