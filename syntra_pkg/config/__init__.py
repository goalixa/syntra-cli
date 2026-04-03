"""Configuration management for Syntra CLI.

This module provides a hierarchical configuration system inspired by Claude's CLI:
1. Built-in defaults (hardcoded)
2. Project config (.syntra/config.local.json)
3. User config (~/.syntra/config.json)
4. Environment variables (SYNTRA_* prefix)

Example:
    from syntra_pkg.config import settings

    # Get a value
    api_url = settings.get("api.base_url")

    # Set a value (persists to user config)
    settings.set("api.base_url", "https://api.syntra.dev")

    # Access nested values
    timeout = settings.api.timeout
"""

from syntra_pkg.config.settings import Settings, settings

__all__ = ["Settings", "settings"]
