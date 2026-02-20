"""
Unit Tests for APIClient

Tests for HTTP client wrapper utility.
"""

from unittest.mock import Mock, patch

import pytest
import requests

from utils.api_client import APIClient


@pytest.mark.unit
class TestAPIClient:
    """Tests for APIClient utility"""

    def test_init_creates_session(self, mock_logger):
        """Test that __init__ creates a requests.Session"""
        client = APIClient(base_url="http://test.com", logger=mock_logger)

        assert client.base_url == "http://test.com"
        assert client.timeout == 10
        assert client.max_retries == 3
        assert client.backoff_base == 1.0
        assert isinstance(client.session, requests.Session)

    def test_init_custom_timeout(self, mock_logger):
        """Test that __init__ accepts custom timeout"""
        client = APIClient(timeout=30, logger=mock_logger)

        assert client.timeout == 30

    def test_init_custom_retry_settings(self, mock_logger):
        """Test that __init__ accepts custom retry settings"""
        client = APIClient(max_retries=5, backoff_base=2.0, logger=mock_logger)

        assert client.max_retries == 5
        assert client.backoff_base == 2.0

    @patch("requests.Session.get")
    def test_get_success_returns_json(self, mock_get, mock_logger):
        """Test that get returns JSON data on successful request"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        result = client.get("/endpoint")

        assert result == {"data": "test"}
        mock_get.assert_called_once()

    @patch("requests.Session.get")
    def test_get_builds_full_url(self, mock_get, mock_logger):
        """Test that get builds full URL from base_url and endpoint"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        client.get("/api/endpoint")

        # Check that the full URL was constructed
        call_args = mock_get.call_args
        assert call_args[0][0] == "http://test.com/api/endpoint"

    @patch("requests.Session.get")
    def test_get_strips_slashes_in_url_construction(self, mock_get, mock_logger):
        """Test that get properly handles slashes in URL construction"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com/", logger=mock_logger)
        client.get("/endpoint")

        # Should not have double slashes
        call_args = mock_get.call_args
        assert call_args[0][0] == "http://test.com/endpoint"

    @patch("requests.Session.get")
    def test_get_passes_params_and_headers(self, mock_get, mock_logger):
        """Test that get passes params and headers to requests"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        params = {"key": "value"}
        headers = {"X-Custom": "header"}
        client.get("/endpoint", params=params, headers=headers)

        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["params"] == params
        assert call_kwargs["headers"] == headers

    @patch("requests.Session.get")
    def test_get_timeout_returns_none(self, mock_get, mock_logger):
        """Test that get returns None on timeout with no retries configured"""
        mock_get.side_effect = requests.exceptions.Timeout()

        client = APIClient(base_url="http://test.com", max_retries=0, logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        mock_logger.error.assert_called()
        assert mock_get.call_count == 1

    @patch("requests.Session.get")
    def test_get_connection_error_returns_none(self, mock_get, mock_logger):
        """Test that get returns None on connection error with no retries configured"""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        client = APIClient(base_url="http://test.com", max_retries=0, logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        mock_logger.error.assert_called()
        assert mock_get.call_count == 1

    @patch("requests.Session.get")
    def test_get_http_error_returns_none(self, mock_get, mock_logger):
        """Test that get returns None on HTTP error (4xx, 5xx)"""
        mock_response = Mock()
        mock_response.status_code = 404
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        mock_logger.error.assert_called()

    @patch("requests.Session.get")
    def test_get_json_decode_error_returns_none(self, mock_get, mock_logger):
        """Test that get returns None on invalid JSON response"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("", "", 0)
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        mock_logger.error.assert_called()
        # JSON errors are not retryable — only one attempt
        assert mock_get.call_count == 1

    @patch("time.sleep")
    @patch("requests.Session.get")
    def test_get_retries_on_timeout(self, mock_get, mock_sleep, mock_logger):
        """Test that get retries the configured number of times on timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()

        client = APIClient(base_url="http://test.com", max_retries=3, logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        assert mock_get.call_count == 4  # 1 initial + 3 retries
        assert mock_sleep.call_count == 3  # sleep before each retry

    @patch("time.sleep")
    @patch("requests.Session.get")
    def test_get_retries_on_connection_error(self, mock_get, mock_sleep, mock_logger):
        """Test that get retries the configured number of times on connection error"""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        client = APIClient(base_url="http://test.com", max_retries=2, logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        assert mock_get.call_count == 3  # 1 initial + 2 retries
        assert mock_sleep.call_count == 2

    @patch("time.sleep")
    @patch("requests.Session.get")
    def test_get_succeeds_on_retry_after_transient_failure(self, mock_get, mock_sleep, mock_logger):
        """Test that get returns data when a retry succeeds after an initial failure"""
        success_response = Mock()
        success_response.json.return_value = {"data": "ok"}
        success_response.raise_for_status = Mock()

        mock_get.side_effect = [requests.exceptions.Timeout(), success_response]

        client = APIClient(base_url="http://test.com", max_retries=3, logger=mock_logger)
        result = client.get("/endpoint")

        assert result == {"data": "ok"}
        assert mock_get.call_count == 2  # failed once, succeeded on first retry
        assert mock_sleep.call_count == 1

    @patch("time.sleep")
    @patch("requests.Session.get")
    def test_get_exponential_backoff_delays(self, mock_get, mock_sleep, mock_logger):
        """Test that backoff delays follow exponential progression: base, 2*base, 4*base"""
        mock_get.side_effect = requests.exceptions.Timeout()

        client = APIClient(
            base_url="http://test.com", max_retries=3, backoff_base=1.0, logger=mock_logger
        )
        client.get("/endpoint")

        sleep_calls = [call.args[0] for call in mock_sleep.call_args_list]
        assert sleep_calls == [1.0, 2.0, 4.0]

    @patch("time.sleep")
    @patch("requests.Session.get")
    def test_get_http_error_does_not_retry(self, mock_get, mock_sleep, mock_logger):
        """Test that HTTP errors (4xx/5xx) are not retried"""
        mock_response = Mock()
        mock_response.status_code = 500
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://test.com", max_retries=3, logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        assert mock_get.call_count == 1  # no retries
        mock_sleep.assert_not_called()

    @patch("requests.Session.post")
    def test_post_success_returns_json(self, mock_post, mock_logger):
        """Test that post returns JSON data on successful request"""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "created"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        result = client.post("/endpoint", json={"data": "test"})

        assert result == {"result": "created"}

    @patch("requests.Session.post")
    def test_post_handles_form_data(self, mock_post, mock_logger):
        """Test that post can send form data"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        form_data = {"field": "value"}
        client.post("/endpoint", data=form_data)

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["data"] == form_data

    def test_set_header_adds_to_session(self, mock_logger):
        """Test that set_header adds header to session"""
        client = APIClient(logger=mock_logger)

        client.set_header("X-API-Key", "secret")

        assert client.session.headers["X-API-Key"] == "secret"

    def test_set_auth_configures_basic_auth(self, mock_logger):
        """Test that set_auth configures basic authentication"""
        client = APIClient(logger=mock_logger)

        client.set_auth("user", "pass")

        assert client.session.auth == ("user", "pass")

    def test_build_url_with_base_url(self, mock_logger):
        """Test that _build_url constructs full URL"""
        client = APIClient(base_url="http://test.com", logger=mock_logger)

        url = client._build_url("/api/data")

        assert url == "http://test.com/api/data"

    def test_build_url_without_base_url(self, mock_logger):
        """Test that _build_url returns endpoint when no base_url"""
        client = APIClient(logger=mock_logger)

        url = client._build_url("http://full.url/endpoint")

        assert url == "http://full.url/endpoint"

    def test_close_closes_session(self, mock_logger):
        """Test that close closes the session"""
        client = APIClient(logger=mock_logger)
        client.session.close = Mock()

        client.close()

        client.session.close.assert_called_once()
