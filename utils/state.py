"""
State Management

Handles persistent state storage for the application.
"""

import json
from typing import Dict, Any
from pathlib import Path


class StateManager:
    """Manages application state persistence"""
    
    def __init__(self, state_file: str = "state.json", logger=None):
        """
        Initialize state manager
        
        Args:
            state_file: Path to state file
            logger: Optional logger instance
        """
        self.state_file = Path(state_file)
        self.logger = logger
        self._state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        """Load state from file"""
        if not self.state_file.exists():
            self._log_info("No existing state file found, starting fresh")
            return {}
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self._log_info(f"Loaded state from {self.state_file}")
                return state
        except Exception as e:
            self._log_error(f"Error loading state file: {e}")
            return {}
    
    def _save_state(self):
        """Save state to file"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self._state, f, indent=2, ensure_ascii=False)
                self._log_info(f"Saved state to {self.state_file}")
        except Exception as e:
            self._log_error(f"Error saving state file: {e}")
    
    def get(self, key: str, default=None) -> Any:
        """
        Get a value from state
        
        Args:
            key: State key
            default: Default value if key doesn't exist
            
        Returns:
            Value from state or default
        """
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set a value in state
        
        Args:
            key: State key
            value: Value to store
        """
        self._state[key] = value
        self._save_state()
    
    def has_changed(self, key: str, new_value: Any) -> bool:
        """
        Check if a value has changed from stored state
        
        Args:
            key: State key
            new_value: New value to compare
            
        Returns:
            True if value has changed or doesn't exist
        """
        old_value = self.get(key)
        has_changed = old_value != new_value
        
        if has_changed:
            self._log_info(f"State changed for '{key}': {old_value} -> {new_value}")
        else:
            self._log_info(f"State unchanged for '{key}': {new_value}")
        
        return has_changed
    
    def clear(self):
        """Clear all state"""
        self._state = {}
        self._save_state()
        self._log_info("State cleared")
    
    def _log_info(self, message: str):
        """Log info message"""
        if self.logger:
            self.logger.info(message)
    
    def _log_error(self, message: str):
        """Log error message"""
        if self.logger:
            self.logger.error(message)
