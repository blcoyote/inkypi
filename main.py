#!/usr/bin/env python3
"""
InkyPi - Main Entry Point

This is the main entry point for the InkyPi display application.
Demonstrates proper separation of concerns with layered architecture.
Runs on startup and updates every hour.
"""

import sys
import time

import schedule
from dotenv import load_dotenv

# Import from organized layers
from core import InkyPiApp
from utils import setup_logger

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = setup_logger(__name__)


def update_display():
    """Update the display - called on schedule"""
    logger.info("=" * 50)
    logger.info("Scheduled update triggered")
    logger.info("=" * 50)
    try:
        with InkyPiApp(logger=logger) as app:
            app.run()
    except ValueError as e:
        logger.error(f"Configuration error: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Error updating display: {e}", exc_info=True)


def main():
    """Main entry point with scheduled updates"""
    logger.info("Starting InkyPi with hourly updates...")

    try:
        # Run immediately on startup with forced update
        logger.info("Running initial update on startup...")
        with InkyPiApp(logger=logger) as app:
            app.run(force_update=True)

        # Schedule to run at the top of every hour (without forced update)
        schedule.every().hour.at(":00").do(update_display)
        logger.info("Scheduled updates at the top of every hour")

        # Keep running and check schedule
        logger.info("Entering main loop (press Ctrl+C to exit)...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
