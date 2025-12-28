"""
Shared Test Fixtures

Global pytest fixtures available to all tests.
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock


@pytest.fixture
def mock_logger():
    """Mock logger that captures log calls without output"""
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    logger.warning = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture
def frozen_time():
    """Fixed datetime for deterministic testing"""
    return datetime(2025, 1, 10, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def sample_address_data():
    """Sample address data matching RenoSyd API structure"""
    return {
        "navn": "Test Location",
        "vejnavn": "Testvej",
        "husnummer": "42",
        "etage": None,
        "sidedør": None,
        "postdistrikt": "TestBy",
        "postnummer": "1234",
        "kvhxcode": "TEST123",
        "kommunenummer": 123,
        "vejkode": 456,
        "breddegrad": 55.6761,
        "laengdegrad": 12.5683,
    }


@pytest.fixture
def sample_standplads_data(sample_address_data):
    """Sample collection point data"""
    return {
        "nummer": "013165",
        "navn": "Test Standplads",
        "beskrivelse": "Test description",
        "adresse": sample_address_data,
        "længdegrad": 12.5683,
        "breddegrad": 55.6761,
        "sidstændret": "2025-01-01T10:00:00Z",
        "beholder": "container",
    }


@pytest.fixture
def sample_planned_collection_data():
    """Sample planned collection data with dynamic future date"""
    future_date = datetime.now(timezone.utc) + timedelta(days=30)
    return {
        "dato": future_date.isoformat().replace("+00:00", "Z"),
        "fraktioner": ["Restaffald", "Papir"],
    }


@pytest.fixture
def sample_api_response(sample_standplads_data, sample_planned_collection_data):
    """Sample API response matching RenoSyd structure with dynamic dates"""
    future_date_2 = datetime.now(timezone.utc) + timedelta(days=60)
    return [
        {
            "standplads": sample_standplads_data,
            "planlagtetømninger": [
                sample_planned_collection_data,
                {
                    "dato": future_date_2.isoformat().replace("+00:00", "Z"),
                    "fraktioner": ["Glas", "Metal"],
                },
            ],
        }
    ]


@pytest.fixture
def sample_waste_schedule(sample_api_response):
    """Parsed WasteSchedule object"""
    from core.models import WasteSchedule

    return WasteSchedule.from_dict(sample_api_response[0])


@pytest.fixture
def mock_inky_display():
    """Mock InkyDisplay for testing"""
    display = Mock()
    display.width = 250
    display.height = 122
    display.WHITE = 0
    display.BLACK = 1
    display.RED = 2
    display.set_border = Mock()
    display.show = Mock()
    display.clear = Mock()
    return display


@pytest.fixture
def temp_state_file(tmp_path):
    """Temporary state file for testing"""
    return tmp_path / "test_state.json"


@pytest.fixture
def mock_requests_session():
    """Mock requests.Session for API testing"""
    session = Mock()
    session.headers = {}
    session.auth = None
    session.get = Mock()
    session.post = Mock()
    session.close = Mock()
    return session


@pytest.fixture
def mock_pil_image():
    """Mock PIL Image for rendering tests"""
    image = Mock()
    image.mode = "P"
    image.size = (250, 122)
    return image


@pytest.fixture
def mock_pil_draw():
    """Mock PIL ImageDraw for rendering tests"""
    draw = Mock()
    draw.text = Mock()
    draw.rectangle = Mock()
    draw.textbbox = Mock(return_value=(0, 0, 100, 20))
    return draw
