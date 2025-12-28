#!/bin/bash
# InkyPi - Linux/Raspberry Pi Setup Script
# This script sets up a Python virtual environment and installs dependencies

echo "========================================"
echo "InkyPi - Linux/Raspberry Pi Setup"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 with:"
    echo "    sudo apt-get update"
    echo "    sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Install system dependencies for InkyPHAT (Raspberry Pi specific)
if [[ -f /etc/rpi-issue ]]; then
    echo "Raspberry Pi detected. Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-pil python3-numpy python3-venv
    
    # Enable SPI if not already enabled
    if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
        echo "Enabling SPI interface..."
        echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
        echo "WARNING: SPI enabled. Please reboot after setup completes."
    fi
    echo ""
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing old venv..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Virtual environment created successfully."
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo ""
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
    echo ""
    echo "Dependencies installed successfully."
else
    echo ""
    echo "WARNING: requirements.txt not found. Skipping dependency installation."
    echo ""
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "    source venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "    deactivate"
echo ""

# Make the script remind user about reboot if needed
if [[ -f /etc/rpi-issue ]] && ! grep -q "^dtparam=spi=on" /boot/config.txt 2>/dev/null; then
    if [ -f /boot/config.txt.backup_inkypi ]; then
        echo "IMPORTANT: Please reboot your Raspberry Pi to enable SPI:"
        echo "    sudo reboot"
        echo ""
    fi
fi
