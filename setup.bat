@echo off
REM InkyPi - Windows Setup Script
REM This script sets up a Python virtual environment and installs dependencies

echo ========================================
echo InkyPi - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or later from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old venv...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully.
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing Windows development dependencies...
if exist requirements-dev.txt (
    pip install -r requirements-dev.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully.
) else if exist requirements.txt (
    echo WARNING: requirements-dev.txt not found, falling back to requirements.txt
    echo Note: Raspberry Pi packages will be skipped on Windows
    pip install -r requirements.txt
    echo.
) else (
    echo WARNING: No requirements file found. Skipping dependency installation.
    echo.
)

REM Create stub modules for Raspberry Pi hardware
echo Creating hardware stub modules for Windows development...
if not exist stubs mkdir stubs
python stubs\create_stubs.py
echo.

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To activate the virtual environment in the future, run:
echo     venv\Scripts\activate.bat
echo.
echo To deactivate, run:
echo     deactivate
echo.
pause
