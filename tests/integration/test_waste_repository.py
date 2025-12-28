"""
Integration Tests for WasteRepository

Tests for waste collection data repository with mocked API.
"""

import pytest
from unittest.mock import Mock, patch
from core.waste_repository import WasteRepository


@pytest.mark.integration
class TestWasteRepository:
    """Integration tests for WasteRepository"""
    
    def test_init_creates_api_client(self, mock_logger):
        """Test that __init__ creates APIClient with correct base URL"""
        repo = WasteRepository(base_url='http://test.com', logger=mock_logger)
        
        assert repo.client is not None
        assert repo.client.base_url == 'http://test.com'
    
    def test_init_uses_default_url_when_none(self, mock_logger):
        """Test that __init__ uses default RenoSyd URL when base_url is None"""
        repo = WasteRepository(logger=mock_logger)
        
        assert repo.client.base_url == repo.DEFAULT_BASE_URL
    
    @patch('core.waste_repository.APIClient.get')
    def test_get_schedule_success_returns_schedules(self, mock_get, sample_api_response, mock_logger):
        """Test that get_schedule returns WasteSchedule objects on success"""
        mock_get.return_value = sample_api_response
        
        repo = WasteRepository(logger=mock_logger)
        schedules = repo.get_schedule('013165')
        
        assert schedules is not None
        assert len(schedules) == 1
        assert schedules[0].standplads.nummer == '013165'
        mock_get.assert_called_once()
    
    @patch('core.waste_repository.APIClient.get')
    def test_get_schedule_builds_correct_endpoint(self, mock_get, sample_api_response, mock_logger):
        """Test that get_schedule calls correct API endpoint"""
        mock_get.return_value = sample_api_response
        
        repo = WasteRepository(logger=mock_logger)
        repo.get_schedule('013165')
        
        # Verify endpoint and params
        call_args = mock_get.call_args
        assert call_args[0][0] == '/api/v1/toemmekalender'
        assert call_args[1]['params'] == {'nummer': '013165'}
    
    @patch('core.waste_repository.APIClient.get')
    def test_get_schedule_api_error_returns_none(self, mock_get, mock_logger):
        """Test that get_schedule returns None on API error"""
        mock_get.return_value = None
        
        repo = WasteRepository(logger=mock_logger)
        schedules = repo.get_schedule('013165')
        
        assert schedules is None
        mock_logger.error.assert_called()
    
    @patch('core.waste_repository.APIClient.get')
    def test_get_schedule_unexpected_format_returns_none(self, mock_get, mock_logger):
        """Test that get_schedule handles unexpected response format"""
        mock_get.return_value = {'unexpected': 'format'}
        
        repo = WasteRepository(logger=mock_logger)
        schedules = repo.get_schedule('013165')
        
        assert schedules is None
        mock_logger.error.assert_called()
    
    @patch('core.waste_repository.APIClient.get')
    def test_get_schedule_parsing_error_handles_gracefully(self, mock_get, mock_logger):
        """Test that get_schedule handles malformed data gracefully"""
        # Data with missing required fields creates empty objects (models have defaults)
        mock_get.return_value = [{'invalid': 'data'}]
        
        repo = WasteRepository(logger=mock_logger)
        schedules = repo.get_schedule('013165')
        
        # Models have defaults, so parsing succeeds but creates empty/default schedule
        assert schedules is not None
        assert len(schedules) == 1
        assert schedules[0].standplads.nummer == ''
    
    @patch('core.waste_repository.APIClient.get')
    def test_get_schedule_multiple_schedules(self, mock_get, sample_api_response, mock_logger):
        """Test that get_schedule handles multiple waste schedules"""
        # Duplicate the response
        mock_get.return_value = sample_api_response + sample_api_response
        
        repo = WasteRepository(logger=mock_logger)
        schedules = repo.get_schedule('013165')
        
        assert schedules is not None
        assert len(schedules) == 2
    
    @patch('core.waste_repository.APIClient.set_header')
    def test_set_api_key_configures_header(self, mock_set_header, mock_logger):
        """Test that set_api_key sets the API key header"""
        repo = WasteRepository(logger=mock_logger)
        
        repo.set_api_key('test-key')
        
        mock_set_header.assert_called_once_with('X-API-Key', 'test-key')
    
    @patch('core.waste_repository.APIClient.set_bearer_token')
    def test_set_bearer_token_configures_auth(self, mock_set_bearer, mock_logger):
        """Test that set_bearer_token configures bearer authentication"""
        repo = WasteRepository(logger=mock_logger)
        
        repo.set_bearer_token('token123')
        
        mock_set_bearer.assert_called_once_with('token123')
    
    @patch('core.waste_repository.APIClient.close')
    def test_close_closes_client(self, mock_close, mock_logger):
        """Test that close closes the API client"""
        repo = WasteRepository(logger=mock_logger)
        
        repo.close()
        
        mock_close.assert_called_once()
