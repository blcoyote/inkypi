"""
API Client for HTTP requests

Provides a simple interface for fetching data from REST APIs.
"""

import time
from typing import Dict, Optional

import requests


class APIClient:
    """HTTP API client with error handling and logging"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 10,
        max_retries: int = 3,
        backoff_base: float = 1.0,
        logger=None,
    ):
        """
        Initialize the API client

        Args:
            base_url: Base URL for all requests (optional)
            timeout: Request timeout in seconds (default: 10)
            max_retries: Number of retry attempts on transient failures (default: 3)
            backoff_base: Base delay in seconds for exponential backoff (default: 1.0)
                          Delay for attempt n = backoff_base * 2^(n-1), e.g. 1s, 2s, 4s
            logger: Optional logger instance
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base
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

        for attempt in range(self.max_retries + 1):
            if attempt > 0:
                delay = self.backoff_base * (2 ** (attempt - 1))
                self._log_info(
                    f"Retry {attempt}/{self.max_retries} for {url} (backoff {delay:.1f}s)..."
                )
                time.sleep(delay)

            try:
                response = self.session.get(
                    url, params=params, headers=headers, timeout=self.timeout
                )
                response.raise_for_status()

                data = response.json()
                self._log_info(f"GET successful: {url}")
                return data

            except requests.exceptions.Timeout:
                self._log_error(
                    f"Request timeout (attempt {attempt + 1}/{self.max_retries + 1}): {url}"
                )

            except requests.exceptions.ConnectionError:
                self._log_error(
                    f"Connection error (attempt {attempt + 1}/{self.max_retries + 1}): {url}"
                )

            except requests.exceptions.HTTPError as e:
                self._log_error(f"HTTP error {e.response.status_code}: {url}")
                return None  # not retryable

            except requests.exceptions.JSONDecodeError:
                self._log_error(f"Invalid JSON response from {url}")
                return None  # not retryable

            except Exception as e:
                self._log_error(f"Unexpected error: {e}")
                return None  # not retryable

        self._log_error(f"All {self.max_retries} retries exhausted for {url}")
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
