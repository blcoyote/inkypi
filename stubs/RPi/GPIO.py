"""
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
