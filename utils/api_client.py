"""
API Client for HTTP requests

Provides a simple interface for fetching data from REST APIs.
"""

import requests
from typing import Dict, Optional


class APIClient:
    """HTTP API client with error handling and logging"""

    def __init__(self, base_url: Optional[str] = None, timeout: int = 10, logger=None):
        """
        Initialize the API client

        Args:
            base_url: Base URL for all requests (optional)
            timeout: Request timeout in seconds (default: 10)
            logger: Optional logger instance
        """
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logger
        self.session = requests.Session()
        self._log_info("APIClient initialized")

    def get(
        self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Make a GET request

        Args:
            endpoint: API endpoint (will be appended to base_url if set)
            params: Query parameters
            headers: HTTP headers

        Returns:
            Dict: JSON response data or None on failure
        """
        url = self._build_url(endpoint)
        self._log_info(f"GET request to {url}")

        try:
            response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            self._log_info(f"GET successful: {url}")
            return data

        except requests.exceptions.Timeout:
            self._log_error(f"Request timeout: {url}")
            return None

        except requests.exceptions.ConnectionError:
            self._log_error(f"Connection error: {url}")
            return None

        except requests.exceptions.HTTPError as e:
            self._log_error(f"HTTP error {e.response.status_code}: {url}")
            return None

        except requests.exceptions.JSONDecodeError:
            self._log_error(f"Invalid JSON response from {url}")
            return None

        except Exception as e:
            self._log_error(f"Unexpected error: {e}")
            return None

    def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """
        Make a POST request

        Args:
            endpoint: API endpoint
            data: Form data
            json: JSON data
            headers: HTTP headers

        Returns:
            Dict: JSON response data or None on failure
        """
        url = self._build_url(endpoint)
        self._log_info(f"POST request to {url}")

        try:
            response = self.session.post(
                url, data=data, json=json, headers=headers, timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            self._log_info(f"POST successful: {url}")
            return result

        except requests.exceptions.Timeout:
            self._log_error(f"Request timeout: {url}")
            return None

        except requests.exceptions.ConnectionError:
            self._log_error(f"Connection error: {url}")
            return None

        except requests.exceptions.HTTPError as e:
            self._log_error(f"HTTP error {e.response.status_code}: {url}")
            return None

        except Exception as e:
            self._log_error(f"Unexpected error: {e}")
            return None

    def set_header(self, key: str, value: str):
        """
        Set a default header for all requests

        Args:
            key: Header name
            value: Header value
        """
        self.session.headers[key] = value
        self._log_info(f"Set header: {key}")

    def set_auth(self, username: str, password: str):
        """
        Set basic authentication

        Args:
            username: Username
            password: Password
        """
        self.session.auth = (username, password)
        self._log_info("Authentication configured")

    def set_bearer_token(self, token: str):
        """
        Set bearer token authentication

        Args:
            token: Bearer token
        """
        self.session.headers["Authorization"] = f"Bearer {token}"
        self._log_info("Bearer token configured")

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from base_url and endpoint"""
        if self.base_url:
            # Remove trailing slash from base_url and leading slash from endpoint
            base = self.base_url.rstrip("/")
            endpoint = endpoint.lstrip("/")
            return f"{base}/{endpoint}"
        return endpoint

    def _log_info(self, message: str):
        """Log info message"""
        if self.logger:
            self.logger.info(message)

    def _log_error(self, message: str):
        """Log error message"""
        if self.logger:
            self.logger.error(message)

    def close(self):
        """Close the session"""
        self.session.close()
        self._log_info("APIClient session closed")
