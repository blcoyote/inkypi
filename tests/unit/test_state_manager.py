"""
Unit Tests for StateManager

Tests for state persistence and change detection.
"""

import pytest
import json
from utils.state import StateManager


@pytest.mark.unit
class TestStateManager:
    """Tests for StateManager utility"""

    def test_init_creates_empty_state_when_file_missing(self, temp_state_file, mock_logger):
        """Test that StateManager initializes with empty state when file doesn't exist"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        assert state._state == {}
        mock_logger.info.assert_called()

    def test_init_loads_existing_state_file(self, temp_state_file, mock_logger):
        """Test that StateManager loads existing state from file"""
        # Create state file with data
        existing_data = {"key1": "value1", "key2": 42}
        with open(temp_state_file, "w") as f:
            json.dump(existing_data, f)

        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        assert state._state == existing_data
        mock_logger.info.assert_called()

    def test_init_handles_corrupt_json_gracefully(self, temp_state_file, mock_logger):
        """Test that StateManager handles corrupt JSON file"""
        # Create corrupt JSON file
        with open(temp_state_file, "w") as f:
            f.write("{ invalid json }")

        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        assert state._state == {}
        mock_logger.error.assert_called()

    def test_get_returns_value_when_exists(self, temp_state_file, mock_logger):
        """Test that get returns stored value"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state._state = {"test_key": "test_value"}

        value = state.get("test_key")

        assert value == "test_value"

    def test_get_returns_default_when_key_missing(self, temp_state_file, mock_logger):
        """Test that get returns default value when key doesn't exist"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        value = state.get("nonexistent", "default_value")

        assert value == "default_value"

    def test_get_returns_none_when_no_default_provided(self, temp_state_file, mock_logger):
        """Test that get returns None when key missing and no default"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        value = state.get("nonexistent")

        assert value is None

    def test_set_stores_value_and_saves_to_file(self, temp_state_file, mock_logger):
        """Test that set stores value and persists to file"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        state.set("test_key", "test_value")

        # Check in-memory state
        assert state._state["test_key"] == "test_value"

        # Check file was saved
        assert temp_state_file.exists()
        with open(temp_state_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data["test_key"] == "test_value"

    def test_set_overwrites_existing_value(self, temp_state_file, mock_logger):
        """Test that set overwrites existing value"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state.set("key", "old_value")

        state.set("key", "new_value")

        assert state.get("key") == "new_value"
        assert state._state["key"] == "new_value"

    def test_has_changed_returns_true_when_value_different(self, temp_state_file, mock_logger):
        """Test that has_changed returns True when value differs"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state._state = {"key": "old_value"}

        changed = state.has_changed("key", "new_value")

        assert changed is True

    def test_has_changed_returns_false_when_value_same(self, temp_state_file, mock_logger):
        """Test that has_changed returns False when value same"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state._state = {"key": "value"}

        changed = state.has_changed("key", "value")

        assert changed is False

    def test_has_changed_returns_true_when_key_missing(self, temp_state_file, mock_logger):
        """Test that has_changed returns True when key doesn't exist"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        changed = state.has_changed("new_key", "value")

        assert changed is True

    def test_has_changed_handles_complex_objects(self, temp_state_file, mock_logger):
        """Test that has_changed compares complex objects correctly"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        old_value = {"nested": {"key": "value"}, "list": [1, 2, 3]}
        state._state = {"key": old_value}

        # Same structure, different object
        new_value = {"nested": {"key": "value"}, "list": [1, 2, 3]}
        changed = state.has_changed("key", new_value)

        assert changed is False

    def test_has_changed_detects_nested_changes(self, temp_state_file, mock_logger):
        """Test that has_changed detects changes in nested structures"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state._state = {"key": {"nested": "value"}}

        changed = state.has_changed("key", {"nested": "different"})

        assert changed is True

    def test_clear_removes_all_state_and_saves(self, temp_state_file, mock_logger):
        """Test that clear removes all state and persists empty state"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state.set("key1", "value1")
        state.set("key2", "value2")

        state.clear()

        assert state._state == {}

        # Verify file was updated
        with open(temp_state_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data == {}

    def test_persistence_across_instances(self, temp_state_file, mock_logger):
        """Test that state persists across different StateManager instances"""
        # First instance sets value
        state1 = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        state1.set("persistent_key", "persistent_value")

        # Second instance loads same file
        state2 = StateManager(state_file=str(temp_state_file), logger=mock_logger)

        assert state2.get("persistent_key") == "persistent_value"

    def test_handles_unicode_data(self, temp_state_file, mock_logger):
        """Test that StateManager handles Unicode/UTF-8 data correctly"""
        state = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        unicode_data = {"danish": "æøå ÆØÅ", "emoji": "🗑️♻️", "special": "tømning"}

        state.set("unicode_test", unicode_data)

        # Reload from file
        state2 = StateManager(state_file=str(temp_state_file), logger=mock_logger)
        loaded_data = state2.get("unicode_test")

        assert loaded_data == unicode_data
