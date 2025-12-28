#!/bin/bash
# InkyPi - Virtual Environment Activation Script
# Quick activation helper for the virtual environment

if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first to create the virtual environment."
    exit 1
fi

echo "Activating InkyPi virtual environment..."
source venv/bin/activate

echo "Virtual environment activated!"
echo "Python: $(which python3)"
echo "To deactivate, run: deactivate"
