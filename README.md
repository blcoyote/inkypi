# InkyPi

A Python application for Raspberry Pi that displays waste collection schedules on an InkyPHAT e-paper display.

## Features

- **Automatic Waste Schedule Tracking** - Fetches next waste collection date and types from RenoSyd API
- **E-Paper Display** - Shows information on InkyPHAT 2.13" display (250x122 pixels)
- **Auto-Update** - Refreshes hourly to keep information current
- **Smart State Management** - Only updates display when data changes to preserve e-paper lifespan
- **Auto-Start on Boot** - Runs automatically when Raspberry Pi starts
- **Cross-Platform Development** - Develop on Windows/Mac with preview images, deploy to Raspberry Pi
- **Adaptive Layout** - Automatically adjusts text size for long waste type names
- **Last Updated Timestamp** - Shows when the display was last refreshed

## Hardware Requirements

- Raspberry Pi (any model with GPIO)
- InkyPHAT 2.13" E-Ink Display (black/white)
- Power supply for Raspberry Pi

## Installation

### On Raspberry Pi

1. Clone or download this project to your Raspberry Pi:
   ```bash
   cd ~
   git clone <repository-url> inkypi
   cd inkypi
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Configure your waste collection address:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Edit the `NUMMER` variable with your address number.

4. The service will start automatically on boot. To start it now:
   ```bash
   sudo systemctl start inkypi
   ```

### On Windows/Mac (Development)

1. Run the setup script:
   ```bash
   # Windows
   setup.bat
   
   # Mac/Linux
   chmod +x setup.sh
   ./setup.sh
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration.

3. Run the application:
   ```bash
   # Windows
   venv\Scripts\activate
   python main.py
   
   # Mac/Linux
   source venv/bin/activate
   python main.py
   ```

   A preview image will be saved as `inky_preview.png`.

## Configuration

Edit the `.env` file to configure:

```env
# RenoSyd waste collection address number
NUMMER=your_address_number_here

# API base URL (optional, uses default if not set)
# BASE_URL=https://skoda-selvbetjeningsapi.renosyd.dk
```

## Project Structure

```
inkypi/
├── main.py                 # Application entry point
├── display/                # Display hardware abstraction
│   ├── __init__.py
│   └── inky_display.py    # InkyPHAT interface
├── rendering/             # Layout and image composition
│   ├── __init__.py
│   ├── renderer.py        # Image rendering utilities
│   └── layouts.py         # Display layout templates
├── core/                  # Business logic
│   ├── __init__.py
│   ├── content_provider.py  # Content formatting
│   ├── models.py          # Data models
│   └── waste_repository.py # API integration
├── utils/                 # Shared utilities
│   ├── __init__.py
│   ├── api_client.py     # HTTP client
│   ├── config.py         # Configuration
│   ├── logger.py         # Logging setup
│   └── state.py          # State management
├── stubs/                # Mock hardware for development
│   └── inky/             # InkyPHAT stubs
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── setup.sh             # Linux/Raspberry Pi setup
├── setup.bat            # Windows setup
└── .env                 # Configuration (not in git)
```

## Architecture

The project follows a layered architecture with separation of concerns:

1. **Display Layer** (`display/`) - Hardware abstraction for InkyPHAT
2. **Rendering Layer** (`rendering/`) - Image composition and layouts
3. **Core Layer** (`core/`) - Business logic and API integration
4. **Utils Layer** (`utils/`) - Shared utilities and helpers

## Service Management (Raspberry Pi)

```bash
# View status
sudo systemctl status inkypi

# View logs
sudo journalctl -u inkypi -f

# Start service
sudo systemctl start inkypi

# Stop service
sudo systemctl stop inkypi

# Restart service
sudo systemctl restart inkypi

# Disable auto-start
sudo systemctl disable inkypi

# Enable auto-start
sudo systemctl enable inkypi
```

## Development

### Activating Virtual Environment

```bash
# Linux/Mac
source activate.sh
# or
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Running Tests

```bash
# Test API connection
python test_waste_repository.py
```

### Code Style

The project uses standard Python conventions:
- PEP 8 style guide
- Type hints where applicable
- Comprehensive docstrings
- Separation of concerns

## Troubleshooting

### Display shows all white
- Check that state.json was deleted to force update
- Verify SPI is enabled: `ls /dev/spi*`
- Check service logs: `sudo journalctl -u inkypi -f`

### Text is too small
- Ensure fonts are installed: `sudo apt-get install fonts-dejavu fonts-liberation`
- Check font loading in logs

### Service won't start
- Check Python path in service: `sudo systemctl cat inkypi`
- Verify virtual environment exists: `ls ~/inkypi/venv`
- Check for errors: `sudo journalctl -u inkypi -n 50`

### API errors
- Verify NUMMER in `.env` is correct
- Check internet connection
- Test API manually: `python test_waste_repository.py`

## Display Rotation

The display is rotated 180 degrees by default to accommodate cable positioning. To change this, edit `display/inky_display.py`:

```python
# Remove or change these lines in __init__:
self._display.h_flip = True
self._display.v_flip = True
```

## License

This project is provided as-is for personal use.

## Credits

- InkyPHAT library by Pimoroni
- RenoSyd API for waste collection data
