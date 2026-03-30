"""CLI configuration and constants with persistent storage."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Default API Configuration
DEFAULT_API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30.0

# CLI Configuration
CLI_NAME = "syntra-cli"
CLI_VERSION = "0.1.0"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / ".env"
USER_CONFIG_DIR = Path.home() / ".syntra"
USER_CONFIG_FILE = USER_CONFIG_DIR / "config.json"

# Colors
PRIMARY_COLOR = "bright_blue"
SUCCESS_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
INFO_COLOR = "cyan"

# Animation settings
SPINNER_STYLE = "dots"
PROGRESS_BAR_STYLE = "bar"


class Config:
    """Configuration manager with persistent storage."""

    def __init__(self):
        """Initialize configuration manager."""
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from user config file."""
        if USER_CONFIG_FILE.exists():
            try:
                with open(USER_CONFIG_FILE, "r") as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._config = {}

    def _save_config(self):
        """Save configuration to user config file."""
        try:
            USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(USER_CONFIG_FILE, "w") as f:
                json.dump(self._config, f, indent=2)
        except IOError:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        # Check environment variable first
        env_value = os.getenv(f"SYNTRA_{key.upper()}")
        if env_value is not None:
            return env_value

        # Then check user config file
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        self._save_config()

    def unset(self, key: str) -> None:
        """
        Remove a configuration value.

        Args:
            key: Configuration key to remove
        """
        if key in self._config:
            del self._config[key]
            self._save_config()

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config.copy()

    @property
    def api_base_url(self) -> str:
        """Get the API base URL."""
        return self.get("api_base_url", DEFAULT_API_BASE_URL)

    def set_api_base_url(self, url: str) -> None:
        """Set the API base URL."""
        self.set("api_base_url", url.rstrip("/"))


# Global configuration instance
config = Config()


# Backward compatibility exports
API_BASE_URL = config.api_base_url
