"""
Waste Collection Repository

Handles fetching waste collection schedule data from the API.
"""

from typing import List, Optional

from utils import APIClient

from .models import WasteSchedule


class WasteRepository:
    """Repository for waste collection schedule data from RenoSyd API"""

    # Default API configuration
    DEFAULT_BASE_URL = "https://skoda-selvbetjeningsapi.renosyd.dk"
    API_VERSION = "v1"

    def __init__(self, base_url: Optional[str] = None, logger=None):
        """
        Initialize the waste repository

        Args:
            base_url: Base URL for the waste collection API (defaults to RenoSyd API)
            logger: Optional logger instance
        """
        self.logger = logger
        if base_url is None:
            base_url = self.DEFAULT_BASE_URL
        self.client = APIClient(base_url=base_url, timeout=15, logger=logger)
        self._log_info(f"WasteRepository initialized with base URL: {base_url}")

    def get_schedule(self, nummer: str) -> Optional[List[WasteSchedule]]:
        """
        Fetch waste collection schedule by collection point number

        Args:
            nummer: Collection point number (e.g., "013165")

        Returns:
            List[WasteSchedule]: List of waste schedules or None on failure
        """
        self._log_info(f"Fetching waste schedule for nummer: {nummer}")

        # Build endpoint based on RenoSyd API structure
        endpoint = f"/api/{self.API_VERSION}/toemmekalender"
        params = {"nummer": nummer}

        # Fetch data from API
        response_data = self.client.get(endpoint, params=params)

        if response_data is None:
            self._log_error("Failed to fetch waste schedule")
            return None

        # Parse response into models
        try:
            if isinstance(response_data, list):
                schedules = [WasteSchedule.from_dict(item) for item in response_data]
                self._log_info(f"Successfully parsed {len(schedules)} waste schedules")
                return schedules
            else:
                self._log_error("Unexpected response format - expected list")
                return None

        except Exception as e:
            self._log_error(f"Error parsing waste schedule data: {e}")
            return None

    def close(self):
        """Close the API client connection"""
        self.client.close()
        self._log_info("WasteRepository closed")

    def _log_info(self, message: str):
        """Log info message"""
        if self.logger:
            self.logger.info(message)

    def _log_error(self, message: str):
        """Log error message"""
        if self.logger:
            self.logger.error(message)
