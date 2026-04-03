"""Settings manager with hierarchical configuration."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from syntra_pkg.config.defaults import get_defaults, THEMES, PROMPT_STYLES
from syntra_pkg.config.schema import SyntraConfig


class Settings:
    """
    Hierarchical settings manager.

    Configuration precedence (highest to lowest):
    1. Environment variables (SYNTRA_* prefix)
    2. User config (~/.syntra/config.json)
    3. Project config (.syntra/config.local.json)
    4. Built-in defaults
    """

    def __init__(self):
        """Initialize settings manager."""
        self._defaults: Dict[str, Any] = get_defaults()
        self._project_config: Dict[str, Any] = {}
        self._user_config: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {}

        # Paths
        self._user_config_dir = Path.home() / ".syntra"
        self._user_config_file = self._user_config_dir / "config.json"
        self._project_config_file = Path.cwd() / ".syntra" / "config.local.json"

        # Load configurations
        self._load_all()

    def _load_all(self) -> None:
        """Load all configuration files."""
        self._load_project_config()
        self._load_user_config()

    def _load_project_config(self) -> None:
        """Load project-local configuration."""
        if self._project_config_file.exists():
            try:
                with open(self._project_config_file, "r") as f:
                    self._project_config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._project_config = {}

    def _load_user_config(self) -> None:
        """Load user configuration."""
        if self._user_config_file.exists():
            try:
                with open(self._user_config_file, "r") as f:
                    self._user_config = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._user_config = {}

    def _save_user_config(self) -> None:
        """Save user configuration to file."""
        try:
            self._user_config_dir.mkdir(parents=True, exist_ok=True)
            with open(self._user_config_file, "w") as f:
                json.dump(self._user_config, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save user config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Dot-separated key (e.g., "api.base_url")
            default: Default value if not found

        Returns:
            Configuration value
        """
        # Check cache first
        if key in self._cache:
            return self._cache[key]

        # Check environment variable
        env_key = f"SYNTRA_{key.replace('.', '_').upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            self._cache[key] = self._parse_env_value(env_value)
            return self._cache[key]

        # Check user config
        value = self._get_nested(self._user_config, key)
        if value is not None:
            self._cache[key] = value
            return value

        # Check project config
        value = self._get_nested(self._project_config, key)
        if value is not None:
            self._cache[key] = value
            return value

        # Check defaults
        value = self._get_nested(self._defaults, key)
        if value is not None:
            self._cache[key] = value
            return value

        return default

    def set(self, key: str, value: Any, persist: bool = True) -> None:
        """
        Set a configuration value.

        Args:
            key: Dot-separated key (e.g., "api.base_url")
            value: Value to set
            persist: Whether to save to user config file
        """
        # Set in user config
        self._set_nested(self._user_config, key, value)
        self._cache[key] = value

        if persist:
            self._save_user_config()

    def unset(self, key: str, persist: bool = True) -> None:
        """
        Remove a configuration value.

        Args:
            key: Dot-separated key to remove
            persist: Whether to save changes to user config file
        """
        self._delete_nested(self._user_config, key)
        if key in self._cache:
            del self._cache[key]

        if persist:
            self._save_user_config()

    def get_all(self, include_defaults: bool = False) -> Dict[str, Any]:
        """
        Get all configuration values.

        Args:
            include_defaults: Whether to include default values

        Returns:
            Dictionary of all configuration values
        """
        result: Dict[str, Any] = {}

        # Start with defaults if requested
        if include_defaults:
            result = self._flatten(self._defaults)

        # Add project config
        result.update(self._flatten(self._project_config))

        # Add user config
        result.update(self._flatten(self._user_config))

        return result

    def reset(self, key: Optional[str] = None) -> None:
        """
        Reset configuration to defaults.

        Args:
            key: Specific key to reset, or None to reset all
        """
        if key is None:
            # Reset all user config
            self._user_config = {}
            self._cache = {}
        else:
            # Reset specific key
            self.unset(key, persist=False)

        self._save_user_config()

    def reload(self) -> None:
        """Reload all configuration files."""
        self._cache = {}
        self._load_all()

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate current configuration.

        Returns:
            Tuple of (is_valid, error_messages)
        """
        try:
            # Build merged config
            merged = self._defaults.copy()
            self._deep_merge(merged, self._project_config)
            self._deep_merge(merged, self._user_config)

            # Validate with Pydantic
            SyntraConfig(**merged)
            return True, []
        except Exception as e:
            return False, [str(e)]

    def export(self) -> str:
        """
        Export current configuration as JSON.

        Returns:
            JSON string of current configuration
        """
        config = self.get_all(include_defaults=True)
        return json.dumps(config, indent=2)

    def import_config(self, config_json: str, merge: bool = True) -> None:
        """
        Import configuration from JSON.

        Args:
            config_json: JSON string to import
            merge: Whether to merge with existing config or replace
        """
        new_config = json.loads(config_json)

        if merge:
            self._deep_merge(self._user_config, new_config)
        else:
            self._user_config = new_config

        self._cache = {}
        self._save_user_config()

    # Helper methods

    def _get_nested(self, data: Dict[str, Any], key: str) -> Any:
        """Get nested value from dictionary using dot notation."""
        keys = key.split(".")
        value = data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
            if value is None:
                return None
        return value

    def _set_nested(self, data: Dict[str, Any], key: str, value: Any) -> None:
        """Set nested value in dictionary using dot notation."""
        keys = key.split(".")
        current = data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def _delete_nested(self, data: Dict[str, Any], key: str) -> bool:
        """Delete nested value from dictionary using dot notation."""
        keys = key.split(".")
        current = data
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                return False
            current = current[k]
        if keys[-1] in current:
            del current[keys[-1]]
            return True
        return False

    def _flatten(self, data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Flatten nested dictionary to dot notation."""
        result = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                result.update(self._flatten(value, full_key))
            else:
                result[full_key] = value
        return result

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Deep merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type."""
        # Try boolean
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False

        # Try number
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        # Return as string
        return value

    # Convenience properties for common settings

    @property
    def api(self) -> APIConfigProxy:
        """API configuration proxy."""
        return APIConfigProxy(self)

    @property
    def cli(self) -> CLIConfigProxy:
        """CLI configuration proxy."""
        return CLIConfigProxy(self)

    @property
    def session(self) -> SessionConfigProxy:
        """Session configuration proxy."""
        return SessionConfigProxy(self)

    @property
    def skills(self) -> SkillsConfigProxy:
        """Skills configuration proxy."""
        return SkillsConfigProxy(self)

    @property
    def output(self) -> OutputConfigProxy:
        """Output configuration proxy."""
        return OutputConfigProxy(self)

    @property
    def dev(self) -> DevConfigProxy:
        """Development configuration proxy."""
        return DevConfigProxy(self)

    @property
    def ui(self) -> UIConfigProxy:
        """UI configuration proxy."""
        return UIConfigProxy(self)


# Configuration proxy classes for convenient access

class ConfigProxy:
    """Base proxy for configuration sections."""

    def __init__(self, settings: Settings, prefix: str):
        self._settings = settings
        self._prefix = prefix

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from this section."""
        return self._settings.get(f"{self._prefix}.{key}", default)

    def set(self, key: str, value: Any) -> None:
        """Set a value in this section."""
        self._settings.set(f"{self._prefix}.{key}", value)


class APIConfigProxy(ConfigProxy):
    """Proxy for API configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "api")

    @property
    def base_url(self) -> str:
        return self.get("base_url")

    @base_url.setter
    def base_url(self, value: str) -> None:
        self.set("base_url", value)

    @property
    def timeout(self) -> float:
        return self.get("timeout", 30.0)

    @timeout.setter
    def timeout(self, value: float) -> None:
        self.set("timeout", value)

    @property
    def max_retries(self) -> int:
        return self.get("max_retries", 3)

    @max_retries.setter
    def max_retries(self, value: int) -> None:
        self.set("max_retries", value)

    @property
    def verify_ssl(self) -> bool:
        return self.get("verify_ssl", True)

    @verify_ssl.setter
    def verify_ssl(self, value: bool) -> None:
        self.set("verify_ssl", value)


class CLIConfigProxy(ConfigProxy):
    """Proxy for CLI configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "cli")

    @property
    def theme(self) -> str:
        return self.get("theme", "default")

    @theme.setter
    def theme(self, value: str) -> None:
        self.set("theme", value)

    @property
    def color_scheme(self) -> str:
        return self.get("color_scheme", "auto")

    @color_scheme.setter
    def color_scheme(self, value: str) -> None:
        self.set("color_scheme", value)

    @property
    def prompt_style(self) -> str:
        return self.get("prompt_style", "fancy")

    @prompt_style.setter
    def prompt_style(self, value: str) -> None:
        self.set("prompt_style", value)

    @property
    def enable_completion(self) -> bool:
        return self.get("enable_completion", True)

    @enable_completion.setter
    def enable_completion(self, value: bool) -> None:
        self.set("enable_completion", value)

    @property
    def editor(self) -> Optional[str]:
        return self.get("editor")

    @editor.setter
    def editor(self, value: str) -> None:
        self.set("editor", value)


class SessionConfigProxy(ConfigProxy):
    """Proxy for session configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "session")

    @property
    def persist_context(self) -> bool:
        return self.get("persist_context", True)

    @persist_context.setter
    def persist_context(self, value: bool) -> None:
        self.set("persist_context", value)

    @property
    def max_history(self) -> int:
        return self.get("max_history", 1000)

    @max_history.setter
    def max_history(self, value: int) -> None:
        self.set("max_history", value)

    @property
    def timeout(self) -> int:
        return self.get("timeout", 1800)

    @timeout.setter
    def timeout(self, value: int) -> None:
        self.set("timeout", value)

    @property
    def auto_save(self) -> bool:
        return self.get("auto_save", True)

    @auto_save.setter
    def auto_save(self, value: bool) -> None:
        self.set("auto_save", value)


class SkillsConfigProxy(ConfigProxy):
    """Proxy for skills configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "skills")

    @property
    def enabled(self) -> list:
        return self.get("enabled", [])

    @enabled.setter
    def enabled(self, value: list) -> None:
        self.set("enabled", value)

    @property
    def paths(self) -> list:
        return self.get("paths", ["~/.syntra/skills", ".syntra/skills"])

    @paths.setter
    def paths(self, value: list) -> None:
        self.set("paths", value)

    @property
    def auto_discover(self) -> bool:
        return self.get("auto_discover", True)

    @auto_discover.setter
    def auto_discover(self, value: bool) -> None:
        self.set("auto_discover", value)


class OutputConfigProxy(ConfigProxy):
    """Proxy for output configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "output")

    @property
    def format(self) -> str:
        return self.get("format", "rich")

    @format.setter
    def format(self, value: str) -> None:
        self.set("format", value)

    @property
    def stream(self) -> bool:
        return self.get("stream", True)

    @stream.setter
    def stream(self, value: bool) -> None:
        self.set("stream", value)

    @property
    def show_metadata(self) -> bool:
        return self.get("show_metadata", False)

    @show_metadata.setter
    def show_metadata(self, value: bool) -> None:
        self.set("show_metadata", value)

    @property
    def timestamp(self) -> bool:
        return self.get("timestamp", False)

    @timestamp.setter
    def timestamp(self, value: bool) -> None:
        self.set("timestamp", value)


class DevConfigProxy(ConfigProxy):
    """Proxy for development configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "dev")

    @property
    def debug(self) -> bool:
        return self.get("debug", False)

    @debug.setter
    def debug(self, value: bool) -> None:
        self.set("debug", value)

    @property
    def log_level(self) -> str:
        return self.get("log_level", "INFO")

    @log_level.setter
    def log_level(self, value: str) -> None:
        self.set("log_level", value)

    @property
    def trace_requests(self) -> bool:
        return self.get("trace_requests", False)

    @trace_requests.setter
    def trace_requests(self, value: bool) -> None:
        self.set("trace_requests", value)


class UIConfigProxy(ConfigProxy):
    """Proxy for UI configuration."""

    def __init__(self, settings: Settings):
        super().__init__(settings, "ui")

    @property
    def spinner_style(self) -> str:
        return self.get("spinner_style", "dots")

    @spinner_style.setter
    def spinner_style(self, value: str) -> None:
        self.set("spinner_style", value)

    @property
    def progress_bar_style(self) -> str:
        return self.get("progress_bar_style", "bar")

    @progress_bar_style.setter
    def progress_bar_style(self, value: str) -> None:
        self.set("progress_bar_style", value)

    @property
    def table_style(self) -> str:
        return self.get("table_style", "rounded")

    @table_style.setter
    def table_style(self, value: str) -> None:
        self.set("table_style", value)


# Global settings instance
settings = Settings()
