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

REM Clone inky library source for IDE support
echo Installing inky library source for IDE support...
if not exist temp_inky (
    echo Cloning inky repository...
    git clone --depth 1 https://github.com/pimoroni/inky.git temp_inky
    if errorlevel 1 (
        echo WARNING: Git clone failed. Skipping IDE support installation.
        echo You can manually download from: https://github.com/pimoroni/inky/tree/main/inky
        goto skip_inky
    )
    
    REM Copy inky source to venv site-packages
    if exist venv\Lib\site-packages (
        echo Copying inky source to venv\Lib\site-packages...
        xcopy /E /I /Y temp_inky\inky venv\Lib\site-packages\inky
        if errorlevel 1 (
            echo WARNING: Failed to copy inky source
        ) else (
            echo Inky source installed successfully for IDE support
        )
    )
    
    REM Cleanup
    echo Cleaning up temporary files...
    rmdir /s /q temp_inky
    
) else (
    echo Inky repository already exists, skipping clone.
)

:skip_inky
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
