"""
Stub modules for Raspberry Pi hardware packages.
This allows development and testing on Windows/Mac without actual hardware.
"""

import os


def create_stub_file(filepath, content):
    """Create a stub Python file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created: {filepath}")


# Get the stubs directory
stubs_dir = os.path.dirname(os.path.abspath(__file__))

# RPi.GPIO stub
rpi_gpio_stub = '''"""
RPi.GPIO stub module for Windows development.
This module provides mock implementations of RPi.GPIO for testing without hardware.
"""

# Constants
BCM = "BCM"
BOARD = "BOARD"
OUT = "OUT"
IN = "IN"
HIGH = 1
LOW = 0
PUD_UP = "PUD_UP"
PUD_DOWN = "PUD_DOWN"
RISING = "RISING"
FALLING = "FALLING"
BOTH = "BOTH"

# Module state
_mode = None
_warnings = True
_pins = {}


def setmode(mode):
    """Set pin numbering mode"""
    global _mode
    _mode = mode
    print(f"[STUB] GPIO.setmode({mode})")


def setwarnings(flag):
    """Enable/disable warnings"""
    global _warnings
    _warnings = flag


def setup(channel, direction, pull_up_down=None, initial=None):
    """Setup a channel"""
    _pins[channel] = {"direction": direction, "state": initial or LOW}
    print(f"[STUB] GPIO.setup({channel}, {direction})")


def output(channel, state):
    """Output to a channel"""
    if channel in _pins:
        _pins[channel]["state"] = state
    print(f"[STUB] GPIO.output({channel}, {state})")


def input(channel):
    """Read from a channel"""
    state = _pins.get(channel, {}).get("state", LOW)
    print(f"[STUB] GPIO.input({channel}) -> {state}")
    return state


def cleanup(channel=None):
    """Cleanup GPIO"""
    if channel:
        _pins.pop(channel, None)
        print(f"[STUB] GPIO.cleanup({channel})")
    else:
        _pins.clear()
        print("[STUB] GPIO.cleanup()")


def add_event_detect(channel, edge, callback=None, bouncetime=None):
    """Add event detection"""
    print(f"[STUB] GPIO.add_event_detect({channel}, {edge})")


def remove_event_detect(channel):
    """Remove event detection"""
    print(f"[STUB] GPIO.remove_event_detect({channel})")
'''

# spidev stub
spidev_stub = '''"""
spidev stub module for Windows development.
"""


class SpiDev:
    """Mock SPI device"""
    
    def __init__(self):
        self.mode = 0
        self.max_speed_hz = 500000
        self.bits_per_word = 8
        print("[STUB] SpiDev created")
    
    def open(self, bus, device):
        """Open SPI device"""
        print(f"[STUB] SpiDev.open({bus}, {device})")
    
    def close(self):
        """Close SPI device"""
        print("[STUB] SpiDev.close()")
    
    def xfer(self, data):
        """Transfer data"""
        print(f"[STUB] SpiDev.xfer({len(data)} bytes)")
        return [0] * len(data)
    
    def xfer2(self, data):
        """Transfer data (variant)"""
        print(f"[STUB] SpiDev.xfer2({len(data)} bytes)")
        return [0] * len(data)
    
    def writebytes(self, data):
        """Write bytes"""
        print(f"[STUB] SpiDev.writebytes({len(data)} bytes)")
    
    def readbytes(self, n):
        """Read bytes"""
        print(f"[STUB] SpiDev.readbytes({n})")
        return [0] * n
'''

# gpiozero stub
gpiozero_stub = '''"""
gpiozero stub module for Windows development.
"""


class Device:
    """Base device class"""
    
    def __init__(self):
        self._closed = False
    
    def close(self):
        """Close device"""
        self._closed = True
        print(f"[STUB] {self.__class__.__name__}.close()")


class LED(Device):
    """Mock LED"""
    
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        self._value = 0
        print(f"[STUB] LED created on pin {pin}")
    
    def on(self):
        """Turn on"""
        self._value = 1
        print(f"[STUB] LED({self.pin}).on()")
    
    def off(self):
        """Turn off"""
        self._value = 0
        print(f"[STUB] LED({self.pin}).off()")
    
    def toggle(self):
        """Toggle state"""
        self._value = 1 - self._value
        print(f"[STUB] LED({self.pin}).toggle() -> {self._value}")


class Button(Device):
    """Mock button"""
    
    def __init__(self, pin, pull_up=True, bounce_time=None):
        super().__init__()
        self.pin = pin
        self.pull_up = pull_up
        self._pressed = False
        print(f"[STUB] Button created on pin {pin}")
    
    @property
    def is_pressed(self):
        """Check if pressed"""
        return self._pressed
    
    def wait_for_press(self, timeout=None):
        """Wait for press"""
        print(f"[STUB] Button({self.pin}).wait_for_press()")
    
    def wait_for_release(self, timeout=None):
        """Wait for release"""
        print(f"[STUB] Button({self.pin}).wait_for_release()")
'''

# inky stub (basic fallback)
inky_stub = '''"""
inky stub module for Windows development.
Provides basic mock for testing without actual InkyPHAT hardware.
"""

from PIL import Image


class InkyPHAT:
    """Mock InkyPHAT display"""
    
    WHITE = 0
    BLACK = 1
    RED = 2
    
    WIDTH = 250
    HEIGHT = 122
    
    def __init__(self, color="black"):
        self.color = color
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.border_color = self.WHITE
        self.h_flip = False
        self.v_flip = False
        print(f"[STUB] InkyPHAT initialized (color={color})")
    
    def set_border(self, color):
        """Set border color"""
        self.border_color = color
        print(f"[STUB] InkyPHAT.set_border({color})")
    
    def set_image(self, image):
        """Set image to display"""
        print(f"[STUB] InkyPHAT.set_image(mode={image.mode}, size={image.size})")
        # Save to file for preview
        try:
            # Convert to RGB for preview display
            if image.mode in ['P', 'L', '1']:
                preview_image = image.convert('RGB')
            else:
                preview_image = image
            
            preview_image.save("inky_preview.png")
            print("[STUB] Saved preview to inky_preview.png")
            print(f"[STUB] Preview stats - min: {image.getextrema()[0]}, max: {image.getextrema()[1]}")
        except Exception as e:
            print(f"[STUB] Could not save preview: {e}")
    
    def show(self):
        """Update display"""
        print("[STUB] InkyPHAT.show() - display updated")


def auto():
    """Auto-detect display"""
    print("[STUB] inky.auto() - returning mock InkyPHAT")
    return InkyPHAT()
'''

# Create stub packages
create_stub_file(os.path.join(stubs_dir, 'RPi', '__init__.py'), '')
create_stub_file(os.path.join(stubs_dir, 'RPi', 'GPIO.py'), rpi_gpio_stub)
create_stub_file(os.path.join(stubs_dir, 'spidev.py'), spidev_stub)
create_stub_file(os.path.join(stubs_dir, 'gpiozero.py'), gpiozero_stub)
create_stub_file(os.path.join(stubs_dir, 'inky', '__init__.py'), inky_stub)
create_stub_file(os.path.join(stubs_dir, 'inky', 'auto.py'), 
                'from . import auto as _auto\nauto = _auto\n')

print("\n" + "="*50)
print("Hardware stubs created successfully!")
print("="*50)
print("\nTo use stubs in your code, add this at the top of your main file:")
print("    import sys")
print("    sys.path.insert(0, 'stubs')")
print("\nOr set PYTHONPATH environment variable:")
print("    set PYTHONPATH=%cd%\\stubs;%PYTHONPATH%")
print("="*50)
