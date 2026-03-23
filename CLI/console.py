"""Console utilities for beautiful terminal output."""

from rich.console import Console
from rich.theme import Theme

# Custom theme for Syntra
custom_theme = Theme(
    {
        "primary": "bright_blue",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "cyan",
        "muted": "dim",
        "header": "bold bright_white",
        "option": "cyan",
        "metadata": "dim cyan",
    }
)

# Create console instance with custom theme
console = Console(theme=custom_theme)

# Also export for convenience
__all__ = ["console"]
