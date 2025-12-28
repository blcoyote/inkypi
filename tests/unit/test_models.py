"""
Unit Tests for Data Models

Tests for Address, Standplads, PlannedCollection, and WasteSchedule models.
"""

import pytest
from datetime import datetime, timezone
from core.models import Address, Standplads, PlannedCollection, WasteSchedule


@pytest.mark.unit
class TestAddress:
    """Tests for Address model"""

    def test_from_dict_valid_data_creates_object(self, sample_address_data):
        """Test that from_dict creates Address from valid data"""
        address = Address.from_dict(sample_address_data)

        assert address.navn == "Test Location"
        assert address.vejnavn == "Testvej"
        assert address.husnummer == "42"
        assert address.postdistrikt == "TestBy"
        assert address.postnummer == "1234"
        assert address.kommunenummer == 123
        assert address.vejkode == 456
        assert address.breddegrad == 55.6761
        assert address.laengdegrad == 12.5683

    def test_from_dict_missing_fields_uses_defaults(self):
        """Test that from_dict handles missing optional fields"""
        minimal_data = {"vejnavn": "Minimalvej", "husnummer": "1"}

        address = Address.from_dict(minimal_data)

        assert address.navn == ""
        assert address.vejnavn == "Minimalvej"
        assert address.husnummer == "1"
        assert address.etage is None
        assert address.sidedør is None
        assert address.kommunenummer == 0
        assert address.breddegrad == 0.0

    def test_from_dict_with_optional_fields(self, sample_address_data):
        """Test that from_dict handles optional fields when present"""
        sample_address_data["etage"] = "2"
        sample_address_data["sidedør"] = "tv"

        address = Address.from_dict(sample_address_data)

        assert address.etage == "2"
        assert address.sidedør == "tv"


@pytest.mark.unit
class TestStandplads:
    """Tests for Standplads (collection point) model"""

    def test_from_dict_valid_data_creates_object(self, sample_standplads_data):
        """Test that from_dict creates Standplads from valid data"""
        standplads = Standplads.from_dict(sample_standplads_data)

        assert standplads.nummer == "013165"
        assert standplads.navn == "Test Standplads"
        assert standplads.beskrivelse == "Test description"
        assert isinstance(standplads.adresse, Address)
        assert standplads.adresse.vejnavn == "Testvej"
        assert standplads.længdegrad == 12.5683
        assert standplads.breddegrad == 55.6761
        assert standplads.beholder == "container"

    def test_from_dict_parses_datetime(self, sample_standplads_data):
        """Test that from_dict correctly parses ISO datetime"""
        standplads = Standplads.from_dict(sample_standplads_data)

        assert isinstance(standplads.sidstændret, datetime)
        assert standplads.sidstændret.year == 2025
        assert standplads.sidstændret.month == 1
        assert standplads.sidstændret.day == 1

    def test_from_dict_invalid_datetime_uses_current_time(self, sample_standplads_data):
        """Test that from_dict handles invalid datetime gracefully"""
        sample_standplads_data["sidstændret"] = "invalid-date"

        standplads = Standplads.from_dict(sample_standplads_data)

        # Should create datetime object (current time as fallback)
        assert isinstance(standplads.sidstændret, datetime)

    def test_from_dict_missing_optional_fields(self, sample_address_data):
        """Test that from_dict handles missing optional fields"""
        minimal_data = {
            "nummer": "123",
            "navn": "Minimal",
            "adresse": sample_address_data,
            "længdegrad": 0.0,
            "breddegrad": 0.0,
            "sidstændret": "2025-01-01T00:00:00Z",
        }

        standplads = Standplads.from_dict(minimal_data)

        assert standplads.nummer == "123"
        assert standplads.beskrivelse is None
        assert standplads.beholder is None


@pytest.mark.unit
class TestPlannedCollection:
    """Tests for PlannedCollection model"""

    def test_from_dict_valid_data_creates_object(self, sample_planned_collection_data):
        """Test that from_dict creates PlannedCollection from valid data"""
        collection = PlannedCollection.from_dict(sample_planned_collection_data)

        assert isinstance(collection.dato, datetime)
        assert collection.fraktioner == ["Restaffald", "Papir"]

    def test_from_dict_parses_datetime_with_timezone(self):
        """Test that from_dict correctly parses timezone-aware datetime"""
        data = {"dato": "2025-01-15T06:00:00Z", "fraktioner": ["Test"]}

        collection = PlannedCollection.from_dict(data)

        assert collection.dato.year == 2025
        assert collection.dato.month == 1
        assert collection.dato.day == 15
        assert collection.dato.hour == 6

    def test_get_date_str_formats_correctly(self, sample_planned_collection_data):
        """Test that get_date_str returns YYYY-MM-DD format"""
        from datetime import timedelta

        collection = PlannedCollection.from_dict(sample_planned_collection_data)
        date_str = collection.get_date_str()

        # Verify format is YYYY-MM-DD (10 characters)
        assert len(date_str) == 10
        assert date_str[4] == "-" and date_str[7] == "-"

        # Verify it's a future date (30 days from now, matching fixture)
        expected_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        assert date_str == expected_date

    def test_get_fractions_str_joins_with_comma(self, sample_planned_collection_data):
        """Test that get_fractions_str joins fractions with comma and space"""
        collection = PlannedCollection.from_dict(sample_planned_collection_data)

        fractions_str = collection.get_fractions_str()

        assert fractions_str == "Restaffald, Papir"

    def test_get_fractions_str_empty_list(self):
        """Test that get_fractions_str handles empty list"""
        data = {"dato": "2025-01-15T06:00:00Z", "fraktioner": []}
        collection = PlannedCollection.from_dict(data)

        fractions_str = collection.get_fractions_str()

        assert fractions_str == ""

    def test_get_fractions_str_single_fraction(self):
        """Test that get_fractions_str handles single fraction"""
        data = {"dato": "2025-01-15T06:00:00Z", "fraktioner": ["Restaffald"]}
        collection = PlannedCollection.from_dict(data)

        fractions_str = collection.get_fractions_str()

        assert fractions_str == "Restaffald"


@pytest.mark.unit
class TestWasteSchedule:
    """Tests for WasteSchedule model"""

    def test_from_dict_valid_data_creates_object(self, sample_api_response):
        """Test that from_dict creates WasteSchedule from valid data"""
        schedule = WasteSchedule.from_dict(sample_api_response[0])

        assert isinstance(schedule.standplads, Standplads)
        assert len(schedule.planlagtetømninger) == 2
        assert all(isinstance(c, PlannedCollection) for c in schedule.planlagtetømninger)

    def test_get_next_collection_returns_future_date(self, sample_api_response):
        """Test that get_next_collection returns upcoming collection"""
        schedule = WasteSchedule.from_dict(sample_api_response[0])

        next_collection = schedule.get_next_collection()

        assert next_collection is not None
        assert isinstance(next_collection, PlannedCollection)
        # Should be in the future (test data has 2025-01-15 and 2025-02-15)
        assert next_collection.dato >= datetime.now(timezone.utc)

    def test_get_next_collection_returns_earliest_future_date(self):
        """Test that get_next_collection returns earliest upcoming collection"""
        from datetime import timedelta

        future_1 = (
            (datetime.now(timezone.utc) + timedelta(days=20)).isoformat().replace("+00:00", "Z")
        )
        future_2 = (
            (datetime.now(timezone.utc) + timedelta(days=30)).isoformat().replace("+00:00", "Z")
        )
        future_3 = (
            (datetime.now(timezone.utc) + timedelta(days=60)).isoformat().replace("+00:00", "Z")
        )

        data = {
            "standplads": {
                "nummer": "123",
                "navn": "Test",
                "adresse": {"vejnavn": "Test", "husnummer": "1"},
                "længdegrad": 0.0,
                "breddegrad": 0.0,
                "sidstændret": "2025-01-01T00:00:00Z",
            },
            "planlagtetømninger": [
                {"dato": future_3, "fraktioner": ["C"]},
                {"dato": future_1, "fraktioner": ["A"]},
                {"dato": future_2, "fraktioner": ["B"]},
            ],
        }
        schedule = WasteSchedule.from_dict(data)

        next_collection = schedule.get_next_collection()

        # Should return earliest future date (future_1 = 20 days from now)
        assert next_collection is not None
        assert next_collection.fraktioner == ["A"]

    def test_get_next_collection_no_future_dates_returns_none(self):
        """Test that get_next_collection returns None when all dates are past"""
        from datetime import timedelta

        past_1 = (
            (datetime.now(timezone.utc) - timedelta(days=365)).isoformat().replace("+00:00", "Z")
        )
        past_2 = (
            (datetime.now(timezone.utc) - timedelta(days=180)).isoformat().replace("+00:00", "Z")
        )

        data = {
            "standplads": {
                "nummer": "123",
                "navn": "Test",
                "adresse": {"vejnavn": "Test", "husnummer": "1"},
                "længdegrad": 0.0,
                "breddegrad": 0.0,
                "sidstændret": "2025-01-01T00:00:00Z",
            },
            "planlagtetømninger": [
                {"dato": past_1, "fraktioner": ["Old"]},
                {"dato": past_2, "fraktioner": ["OldToo"]},
            ],
        }
        schedule = WasteSchedule.from_dict(data)

        next_collection = schedule.get_next_collection()

        assert next_collection is None

    def test_get_next_collection_empty_list_returns_none(self):
        """Test that get_next_collection returns None when no collections exist"""
        data = {
            "standplads": {
                "nummer": "123",
                "navn": "Test",
                "adresse": {"vejnavn": "Test", "husnummer": "1"},
                "længdegrad": 0.0,
                "breddegrad": 0.0,
                "sidstændret": "2025-01-01T00:00:00Z",
            },
            "planlagtetømninger": [],
        }
        schedule = WasteSchedule.from_dict(data)

        next_collection = schedule.get_next_collection()

        assert next_collection is None

    def test_get_collections_for_date_filters_by_date(self):
        """Test that get_collections_for_date returns only matching date"""
        data = {
            "standplads": {
                "nummer": "123",
                "navn": "Test",
                "adresse": {"vejnavn": "Test", "husnummer": "1"},
                "længdegrad": 0.0,
                "breddegrad": 0.0,
                "sidstændret": "2025-01-01T00:00:00Z",
            },
            "planlagtetømninger": [
                {"dato": "2025-01-15T06:00:00Z", "fraktioner": ["A"]},
                {"dato": "2025-01-15T12:00:00Z", "fraktioner": ["B"]},
                {"dato": "2025-01-16T06:00:00Z", "fraktioner": ["C"]},
            ],
        }
        schedule = WasteSchedule.from_dict(data)

        target_date = datetime(2025, 1, 15, tzinfo=timezone.utc)
        collections = schedule.get_collections_for_date(target_date)

        assert len(collections) == 2
        assert all(c.dato.strftime("%Y-%m-%d") == "2025-01-15" for c in collections)

    def test_get_collections_for_date_no_matches(self):
        """Test that get_collections_for_date returns empty list when no matches"""
        data = {
            "standplads": {
                "nummer": "123",
                "navn": "Test",
                "adresse": {"vejnavn": "Test", "husnummer": "1"},
                "længdegrad": 0.0,
                "breddegrad": 0.0,
                "sidstændret": "2025-01-01T00:00:00Z",
            },
            "planlagtetømninger": [
                {"dato": "2025-01-15T06:00:00Z", "fraktioner": ["A"]},
            ],
        }
        schedule = WasteSchedule.from_dict(data)

        target_date = datetime(2025, 1, 20, tzinfo=timezone.utc)
        collections = schedule.get_collections_for_date(target_date)

        assert collections == []
