#!/usr/bin/env python3
"""
InkyPi - Main Entry Point

This is the main entry point for the InkyPi display application.
Demonstrates proper separation of concerns with layered architecture.
Runs on startup and updates every hour.
"""

import sys
import os
import time
import schedule

# Import from organized layers
from display import InkyDisplay
from rendering import Renderer, Layouts
from core import ContentProvider, WasteRepository
from utils import setup_logger, StateManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = setup_logger(__name__)


class InkyPiApp:
    """Main application class demonstrating separation of concerns"""
    
    def __init__(self):
        """Initialize the InkyPi application with dependency injection"""
        logger.info("Initializing InkyPi application...")
        
        # Initialize layers with dependency injection
        self.display = InkyDisplay(logger=logger)
        self.renderer = Renderer(
            width=self.display.width,
            height=self.display.height,
            logger=logger
        )
        self.layouts = Layouts(
            width=self.display.width,
            height=self.display.height,
            logger=logger
        )
        self.content = ContentProvider(logger=logger)
        self.waste_repo = WasteRepository(logger=logger)
        self.state = StateManager(state_file="state.json", logger=logger)
        
        # Get configuration from environment
        self.nummer = os.getenv('NUMMER', '013165')
        
        logger.info("All layers initialized successfully")
    
    def clear_to_white(self):
        """Clear the display to white"""
        logger.info("Clearing display to white...")
        self.display.clear(color=InkyDisplay.WHITE)
        logger.info("Display cleared to white successfully")
    
    def show_title_and_date(self, title, date):
        """
        Display a two-section layout with title and date
        
        Args:
            title: Title text for top section
            date: Date text for bottom section
        """
        logger.info(f"Rendering title and date: '{title}' / '{date}'")
        
        # Create the layout
        image = self.layouts.title_and_date(title, date)
        
        # Display on InkyPHAT
        self.display.set_border(InkyDisplay.WHITE)
        self.display.show(image)
        
        logger.info("Title and date displayed successfully")
    
    def show_next_waste_pickup(self):
        """
        Fetch and display the next waste collection
        Shows waste types in title field and date in date field
        Only updates display if data has changed
        """
        logger.info("Fetching next waste pickup...")
        
        try:
            # Fetch waste schedule
            schedules = self.waste_repo.get_schedule(nummer=self.nummer)
            
            if not schedules:
                logger.error("No waste schedule data available")
                # Check if we need to update display
                error_state = {"status": "no_data", "date": self.content.get_current_date()}
                if self.state.has_changed('last_display', error_state):
                    self.show_title_and_date("No Data", error_state["date"])
                    self.state.set('last_display', error_state)
                else:
                    logger.info("Display unchanged (no data state)")
                return
            
            # Get next collection
            schedule = schedules[0]
            next_collection = schedule.get_next_collection()
            
            if not next_collection:
                logger.warning("No upcoming waste collections found")
                error_state = {"status": "no_pickups", "date": self.content.get_current_date()}
                if self.state.has_changed('last_display', error_state):
                    self.show_title_and_date("No Pickups", error_state["date"])
                    self.state.set('last_display', error_state)
                else:
                    logger.info("Display unchanged (no pickups state)")
                return
            
            # Format the display data
            waste_types = next_collection.get_fractions_str()
            # Remove truncation - let the layout handle long titles
            # if len(waste_types) > 40:
            #     waste_types = waste_types[:37] + "..."
            
            collection_date = next_collection.get_date_str()
            
            # Create state object for comparison
            current_state = {
                "status": "success",
                "waste_types": waste_types,
                "collection_date": collection_date,
                "fractions": next_collection.fraktioner  # Store full list for comparison
            }
            
            # Only update display if data has changed
            if self.state.has_changed('last_display', current_state):
                logger.info(f"Data changed - updating display: {waste_types} on {collection_date}")
                self.show_title_and_date(waste_types, collection_date)
                self.state.set('last_display', current_state)
            else:
                logger.info(f"Data unchanged - skipping display update: {waste_types} on {collection_date}")
            
        except Exception as e:
            logger.error(f"Error fetching waste pickup data: {e}", exc_info=True)
            error_state = {"status": "error", "message": str(e), "date": self.content.get_current_date()}
            if self.state.has_changed('last_display', error_state):
                self.show_title_and_date("Error", error_state["date"])
                self.state.set('last_display', error_state)
    
    def run(self):
        """Main application run method - updates the display"""
        logger.info("Running InkyPi application...")
        
        # Show next waste pickup
        self.show_next_waste_pickup()
        
        logger.info("Application completed successfully")


def update_display():
    """Update the display - called on schedule"""
    try:
        app = InkyPiApp()
        app.run()
    except Exception as e:
        logger.error(f"Error updating display: {e}", exc_info=True)


def main():
    """Main entry point with scheduled updates"""
    logger.info("Starting InkyPi with hourly updates...")
    
    try:
        # Run immediately on startup
        logger.info("Running initial update...")
        update_display()
        
        # Schedule to run every hour
        schedule.every().hour.do(update_display)
        logger.info("Scheduled updates every hour")
        
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
