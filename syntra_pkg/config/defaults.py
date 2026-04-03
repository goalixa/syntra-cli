"""Default configuration values for Syntra CLI.

These are the built-in defaults that are used when no other configuration
is provided. They can be overridden by project config, user config, or
environment variables.
"""

from typing import Dict, Any


def get_defaults() -> Dict[str, Any]:
    """
    Get default configuration values.

    Returns:
        Dictionary of default configuration values
    """
    return {
        # API Configuration
        "api": {
            "base_url": "http://localhost:8000",
            "timeout": 30.0,
            "max_retries": 3,
            "verify_ssl": True,
        },

        # CLI Configuration
        "cli": {
            "theme": "default",
            "color_scheme": "auto",
            "prompt_style": "fancy",
            "enable_completion": True,
            "editor": None,  # Uses $EDITOR if not set
        },

        # Session Configuration
        "session": {
            "persist_context": True,
            "max_history": 1000,
            "timeout": 1800,  # 30 minutes
            "auto_save": True,
        },

        # Skill Configuration
        "skills": {
            "enabled": ["ask", "chat", "config", "health", "agents"],
            "paths": ["~/.syntra/skills", ".syntra/skills"],
            "auto_discover": True,
        },

        # Output Configuration
        "output": {
            "format": "rich",  # rich, json, markdown, plain
            "stream": True,
            "show_metadata": False,
            "timestamp": False,
        },

        # Development Configuration
        "dev": {
            "debug": False,
            "log_level": "INFO",
            "trace_requests": False,
        },

        # UI Configuration
        "ui": {
            "spinner_style": "dots",
            "progress_bar_style": "bar",
            "table_style": "rounded",
        },
    }


# Theme definitions
THEMES = {
    "default": {
        "primary": "bright_blue",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "cyan",
        "muted": "dim",
        "header": "bold bright_white",
        "option": "cyan",
        "metadata": "dim cyan",
    },
    "dark": {
        "primary": "#67b7e1",
        "success": "#6a9f58",
        "warning": "#d5a637",
        "error": "#e06c75",
        "info": "#61afef",
        "muted": "dim",
        "header": "bold white",
        "option": "#61afef",
        "metadata": "dim #61afef",
    },
    "light": {
        "primary": "blue",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "cyan",
        "muted": "grey50",
        "header": "bold black",
        "option": "cyan",
        "metadata": "grey50 cyan",
    },
    "minimal": {
        "primary": "white",
        "success": "white",
        "warning": "white",
        "error": "white",
        "info": "white",
        "muted": "dim",
        "header": "bold",
        "option": "white",
        "metadata": "dim",
    },
    "hacker": {
        "primary": "bright_green",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "info": "bright_green",
        "muted": "dim green",
        "header": "bold bright_green",
        "option": "bright_green",
        "metadata": "dim bright_green",
    },
}

# Prompt styles
PROMPT_STYLES = {
    "fancy": "{style}syntra{style} {{count}} > ",
    "minimal": "> ",
    "context": "{style}syntra{style} [{context}] {{count}} > ",
    "custom": "{icon} {style}syntra{style} > ",
}
