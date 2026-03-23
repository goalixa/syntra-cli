"""CLI configuration and constants."""

from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30.0

# CLI Configuration
CLI_NAME = "syntra"
CLI_VERSION = "0.1.0"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / ".env"

# Colors
PRIMARY_COLOR = "bright_blue"
SUCCESS_COLOR = "green"
WARNING_COLOR = "yellow"
ERROR_COLOR = "red"
INFO_COLOR = "cyan"

# Animation settings
SPINNER_STYLE = "dots"
PROGRESS_BAR_STYLE = "bar"
