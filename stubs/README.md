# InkyPi Development Stubs

This directory contains stub implementations of Raspberry Pi-specific hardware modules for Windows/Mac development.

## Included Stubs

- **RPi.GPIO** - GPIO pin control
- **spidev** - SPI device communication  
- **gpiozero** - High-level GPIO interface
- **inky** - Basic InkyPHAT mock (saves preview to PNG)

## Usage

### Method 1: Add to sys.path (in your code)
```python
import sys
import os

# Add stubs to path on non-Raspberry Pi systems
if not os.path.exists('/etc/rpi-issue'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'stubs'))

# Now import normally
from inky.auto import auto
import RPi.GPIO as GPIO
```

### Method 2: Set PYTHONPATH
```bash
# Windows
set PYTHONPATH=%cd%\stubs;%PYTHONPATH%

# Linux/Mac
export PYTHONPATH="$(pwd)/stubs:$PYTHONPATH"
```

### Method 3: Conditional imports
```python
try:
    from inky.auto import auto
except ImportError:
    import sys
    sys.path.insert(0, 'stubs')
    from inky.auto import auto
```

## Features

All stub modules print their actions to console with `[STUB]` prefix, making it easy to track hardware calls during development.

The InkyPHAT stub saves display output to `inky_preview.png` so you can see what would be displayed.

## Regenerating Stubs

Run `create_stubs.py` to regenerate all stub modules:
```bash
python stubs\create_stubs.py
```
