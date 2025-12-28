"""
Unit Tests for APIClient

Tests for HTTP client wrapper utility.
"""

import pytest
from unittest.mock import Mock, patch
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
        assert isinstance(client.session, requests.Session)

    def test_init_custom_timeout(self, mock_logger):
        """Test that __init__ accepts custom timeout"""
        client = APIClient(timeout=30, logger=mock_logger)

        assert client.timeout == 30

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
        """Test that get returns None on timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        mock_logger.error.assert_called()

    @patch("requests.Session.get")
    def test_get_connection_error_returns_none(self, mock_get, mock_logger):
        """Test that get returns None on connection error"""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        client = APIClient(base_url="http://test.com", logger=mock_logger)
        result = client.get("/endpoint")

        assert result is None
        mock_logger.error.assert_called()

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

    def test_set_bearer_token_sets_authorization_header(self, mock_logger):
        """Test that set_bearer_token sets Authorization header"""
        client = APIClient(logger=mock_logger)

        client.set_bearer_token("token123")

        assert client.session.headers["Authorization"] == "Bearer token123"

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
