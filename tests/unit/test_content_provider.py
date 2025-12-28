"""
Unit Tests for ContentProvider

Tests for content formatting utilities.
"""

import pytest
from datetime import datetime
from unittest.mock import patch
from core.content_provider import ContentProvider


@pytest.mark.unit
class TestContentProvider:
    """Tests for ContentProvider utility"""

    def test_init_creates_instance(self, mock_logger):
        """Test that __init__ creates ContentProvider instance"""
        provider = ContentProvider(logger=mock_logger)

        assert provider.logger == mock_logger
        mock_logger.info.assert_called()

    def test_get_welcome_message_returns_string(self, mock_logger):
        """Test that get_welcome_message returns welcome text"""
        provider = ContentProvider(logger=mock_logger)

        message = provider.get_welcome_message()

        assert message == "InkyPi Display Ready"
        assert isinstance(message, str)

    @patch("core.content_provider.datetime")
    def test_get_current_time_formats_correctly(self, mock_datetime, mock_logger):
        """Test that get_current_time returns HH:MM:SS format"""
        mock_datetime.now.return_value = datetime(2025, 1, 10, 14, 30, 45)
        provider = ContentProvider(logger=mock_logger)

        time_str = provider.get_current_time()

        assert time_str == "14:30:45"

    @patch("core.content_provider.datetime")
    def test_get_current_date_formats_correctly(self, mock_datetime, mock_logger):
        """Test that get_current_date returns YYYY-MM-DD format"""
        mock_datetime.now.return_value = datetime(2025, 1, 10, 14, 30, 45)
        provider = ContentProvider(logger=mock_logger)

        date_str = provider.get_current_date()

        assert date_str == "2025-01-10"

    def test_format_temperature_formats_one_decimal(self, mock_logger):
        """Test that format_temperature formats to one decimal place"""
        provider = ContentProvider(logger=mock_logger)

        temp_str = provider.format_temperature(22.5)

        assert temp_str == "22.5°C"

    def test_format_temperature_rounds_correctly(self, mock_logger):
        """Test that format_temperature rounds to one decimal"""
        provider = ContentProvider(logger=mock_logger)

        temp_str = provider.format_temperature(22.567)

        assert temp_str == "22.6°C"

    def test_format_temperature_handles_negative(self, mock_logger):
        """Test that format_temperature handles negative temperatures"""
        provider = ContentProvider(logger=mock_logger)

        temp_str = provider.format_temperature(-5.3)

        assert temp_str == "-5.3°C"

    def test_format_temperature_handles_zero(self, mock_logger):
        """Test that format_temperature handles zero temperature"""
        provider = ContentProvider(logger=mock_logger)

        temp_str = provider.format_temperature(0.0)

        assert temp_str == "0.0°C"
