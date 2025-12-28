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
    sudo apt-get install -y python3-pip python3-pil python3-numpy python3-venv fonts-dejavu fonts-liberation
    
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

# Setup auto-start on Raspberry Pi
if [[ -f /etc/rpi-issue ]]; then
    echo "========================================"
    echo "Configuring Auto-Start on Boot"
    echo "========================================"
    echo ""
    
    # Get the absolute path to the project directory
    PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PYTHON_PATH="$PROJECT_DIR/venv/bin/python3"
    MAIN_SCRIPT="$PROJECT_DIR/main.py"
    SERVICE_NAME="inkypi"
    SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
    
    echo "Creating systemd service..."
    
    # Create systemd service file
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=InkyPi Display Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PYTHON_PATH $MAIN_SCRIPT
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    if [ $? -eq 0 ]; then
        echo "Service file created successfully."
        
        # Reload systemd to recognize new service
        echo "Reloading systemd daemon..."
        sudo systemctl daemon-reload
        
        # Enable service to start on boot
        echo "Enabling service to start on boot..."
        sudo systemctl enable "$SERVICE_NAME.service"
        
        echo ""
        echo "✓ Auto-start configured successfully!"
        echo ""
        echo "Service commands:"
        echo "  Start now:    sudo systemctl start $SERVICE_NAME"
        echo "  Stop:         sudo systemctl stop $SERVICE_NAME"
        echo "  Restart:      sudo systemctl restart $SERVICE_NAME"
        echo "  Status:       sudo systemctl status $SERVICE_NAME"
        echo "  View logs:    sudo journalctl -u $SERVICE_NAME -f"
        echo "  Disable:      sudo systemctl disable $SERVICE_NAME"
        echo ""
        
        # Ask if user wants to start now
        read -p "Do you want to start the service now? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo systemctl start "$SERVICE_NAME"
            echo "Service started. Check status with: sudo systemctl status $SERVICE_NAME"
        else
            echo "Service will start automatically on next boot."
        fi
        echo ""
    else
        echo "ERROR: Failed to create service file"
    fi
fi

# Remind user about reboot if SPI was enabled
if [[ -f /etc/rpi-issue ]] && ! grep -q "^dtparam=spi=on" /boot/firmware/config.txt 2>/dev/null && ! grep -q "^dtparam=spi=on" /boot/config.txt 2>/dev/null; then
    echo "========================================"
    echo "IMPORTANT: Reboot Required"
    echo "========================================"
    echo "SPI interface was enabled. Please reboot your Raspberry Pi:"
    echo "    sudo reboot"
    echo ""
fi
