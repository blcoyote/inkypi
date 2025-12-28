"""
Waste Collection Repository

Handles fetching waste collection schedule data from the API.
"""

from typing import List, Optional
from .models import WasteSchedule
from utils import APIClient


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
        params = {'nummer': nummer}
        
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
    
    def get_schedule_by_address(self, address: str) -> Optional[List[WasteSchedule]]:
        """
        Fetch waste collection schedule by address
        Note: This endpoint may not be available in the RenoSyd API
        
        Args:
            address: Address to search for
            
        Returns:
            List[WasteSchedule]: List of waste schedules or None on failure
        """
        self._log_info(f"Fetching waste schedule for address: {address}")
        
        # Note: Adjust endpoint if address search becomes available
        endpoint = f"/api/{self.API_VERSION}/toemmekalender/search"
        params = {'address': address}
        
        response_data = self.client.get(endpoint, params=params)
        
        if response_data is None:
            self._log_error("Failed to fetch waste schedule by address")
            return None
        
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
    
    def set_api_key(self, api_key: str):
        """
        Set API key for authentication
        
        Args:
            api_key: API key for the waste collection service
        """
        self.client.set_header('X-API-Key', api_key)
        self._log_info("API key configured")
    
    def set_bearer_token(self, token: str):
        """
        Set bearer token for authentication
        
        Args:
            token: Bearer token
        """
        self.client.set_bearer_token(token)
        self._log_info("Bearer token configured")
    
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
