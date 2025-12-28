"""
Application Orchestrator

Main application class that coordinates all layers and manages the display workflow.
"""

import os
from typing import Dict, Any
from display import InkyDisplay
from rendering import Layouts
from .content_provider import ContentProvider
from .waste_repository import WasteRepository
from utils import StateManager

# Constants
STATE_LAST_DISPLAY = "last_display"


class InkyPiApp:
    """Main application class demonstrating separation of concerns"""

    def __init__(self, logger=None, state_file: str = "state.json"):
        """Initialize the InkyPi application with dependency injection

        Args:
            logger: Optional logger instance
            state_file: Path to state file (default: state.json)
        """
        self.logger = logger
        self._log_info("Initializing InkyPi application...")

        # Initialize layers with dependency injection
        self.display = InkyDisplay(logger=logger)
        self.layouts = Layouts(width=self.display.width, height=self.display.height, logger=logger)
        self.content = ContentProvider(logger=logger)
        self.waste_repo = WasteRepository(logger=logger)
        self.state = StateManager(state_file=state_file, logger=logger)

        # Get configuration from environment with validation
        self.nummer = os.getenv("NUMMER") or ""
        if not self.nummer:
            raise ValueError("NUMMER environment variable is required")

        self._log_info("All layers initialized successfully")

    def clear_to_white(self):
        """Clear the display to white"""
        self._log_info("Clearing display to white...")
        self.display.clear(color=InkyDisplay.WHITE)
        self._log_info("Display cleared to white successfully")

    def show_title_and_date(self, title, date):
        """
        Display a two-section layout with title and date

        Args:
            title: Title text for top section
            date: Date text for bottom section
        """
        self._log_info(f"Rendering title and date: '{title}' / '{date}'")

        # Create the layout
        image = self.layouts.title_and_date(title, date)

        # Display on InkyPHAT
        self.display.set_border(InkyDisplay.WHITE)
        self.display.show(image)

        self._log_info("Title and date displayed successfully")

    def show_next_waste_pickup(self):
        """
        Fetch and display the next waste collection
        Shows waste types in title field and date in date field
        Only updates display if data has changed
        """
        self._log_info("Fetching next waste pickup...")

        try:
            # Fetch waste schedule
            schedules = self.waste_repo.get_schedule(nummer=self.nummer)

            if not schedules:
                self._log_error("No waste schedule data available")
                error_state = {"status": "no_data", "date": self.content.get_current_date()}
                self._handle_error_state(error_state, "No Data")
                return

            # Get next collection
            schedule = schedules[0]
            next_collection = schedule.get_next_collection()

            if not next_collection:
                self._log_warning("No upcoming waste collections found")
                error_state = {"status": "no_pickups", "date": self.content.get_current_date()}
                self._handle_error_state(error_state, "No Pickups")
                return

            # Format the display data
            waste_types = next_collection.get_fractions_str()
            collection_date = next_collection.get_date_str()

            # Create state object for comparison
            current_state = {
                "status": "success",
                "waste_types": waste_types,
                "collection_date": collection_date,
                "fractions": next_collection.fraktioner,  # Store full list for comparison
            }

            # Only update display if data has changed
            if self.state.has_changed(STATE_LAST_DISPLAY, current_state):
                self._log_info(
                    f"Data changed - updating display: {waste_types} on {collection_date}"
                )
                self.show_title_and_date(waste_types, collection_date)
                self.state.set(STATE_LAST_DISPLAY, current_state)
            else:
                self._log_info(
                    f"Data unchanged - skipping display update: {waste_types} on {collection_date}"
                )

        except Exception as e:
            self._log_error(f"Error fetching waste pickup data: {e}", exc_info=True)
            error_state = {
                "status": "error",
                "message": str(e),
                "date": self.content.get_current_date(),
            }
            self._handle_error_state(error_state, "Error")

    def run(self):
        """Main application run method - updates the display"""
        self._log_info("Running InkyPi application...")

        # Show next waste pickup
        self.show_next_waste_pickup()

        self._log_info("Application completed successfully")

    def close(self):
        """Cleanup resources"""
        if hasattr(self, "waste_repo"):
            self.waste_repo.close()
        self._log_info("InkyPiApp resources cleaned up")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False

    def _handle_error_state(self, error_state: Dict[str, Any], title: str):
        """Handle error state display update

        Args:
            error_state: State dictionary for the error
            title: Title to display on error
        """
        if self.state.has_changed(STATE_LAST_DISPLAY, error_state):
            self.show_title_and_date(
                title, error_state.get("date", self.content.get_current_date())
            )
            self.state.set(STATE_LAST_DISPLAY, error_state)
        else:
            self._log_info(f"Display unchanged ({error_state['status']} state)")

    def _log_info(self, message: str):
        """Log info message"""
        if self.logger:
            self.logger.info(message)

    def _log_error(self, message, exc_info=False):
        """Log error message"""
        if self.logger:
            self.logger.error(message, exc_info=exc_info)

    def _log_warning(self, message):
        """Log warning message"""
        if self.logger:
            self.logger.warning(message)
